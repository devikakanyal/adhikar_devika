from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from web3 import Web3
import json
import os
from django.shortcuts import render
from .models import Post , Lawyer  # Make sure this is your actual model
from django.utils import timezone
from django.db.models import Q

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import chat_utils



# Connect to local blockchain (Hardhat network)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Change if needed

# Load ABI
abi_path = os.path.join(settings.BASE_DIR, 'backend/fir', 'contract_abi.json')
with open(abi_path, 'r') as f:
    abi = json.load(f)

# Blockchain details — from settings.py
contract_address = settings.CONTRACT_ADDRESS
public_address = settings.BLOCKCHAIN_ADDRESS
private_key = settings.BLOCKCHAIN_PRIVATE_KEY

contract = w3.eth.contract(address=contract_address, abi=abi)

# View to render FIR submission form

def home(request):
    return render( request , "fir/template/home.html")
def fir(request):
    return render(request, "fir/template/fir.html")

def find_help(request):
    
    query = request.GET.get('location', '')
    results = []

    if query:
        results = Lawyer.objects.filter(
            Q(pin_code__icontains=query) |
            Q(city__icontains=query)
        ).order_by('-verified', '-rating')

    return render(request, 'fir/template/find_help.html', {'results': results, 'query': query})
    # return render(request , "fir/template/find_help.html")    

def login(request):
    return render( request , "fir/template/login.html") 



def support_forum(request):
    posts = Post.objects.all().order_by('-created_at')  # Newest posts first
    return render(request, 'fir/template/support_forum.html', {'posts': posts})

def new_post(request):
    return render( request , 'fir/template/new_post.html')


# Store chat sessions
chat_sessions = {}


def chatbot(request):
    # Initialize a new session if needed
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    # Create a new chat session if one doesn't exist
    if session_id not in chat_sessions:
        chat_sessions[session_id] = chat_utils.initialize_chat()
    
    return render(request, 'fir/template/chatbot.html')


@csrf_exempt
def get_chatbot_response(request):
    if request.method == 'POST':
        try:
            # Get the user message from the request
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get or create chat session
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            
            if session_id not in chat_sessions:
                chat_sessions[session_id] = chat_utils.initialize_chat()
            
            # Get response from the chatbot
            response = chat_utils.get_response(chat_sessions[session_id], user_message)
            
            return JsonResponse({'response': response})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)    

# View to handle form submission
def submit_fir(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        ipfs_hash = request.POST.get('ipfs', 'NA')

        nonce = w3.eth.get_transaction_count(public_address)

        txn = contract.functions.fileFIR(name, desc, ipfs_hash).build_transaction({
            'from': public_address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.to_wei('5', 'gwei')
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return render(request, 'fir/template/success.html', {'tx_hash': tx_hash.hex()} )

    # return render(request, "fir/fir_form.html")


def view_firs(request):
        firs = []
        fir_count = contract.functions.firCount().call()

        for i in range(fir_count):
            fir = contract.functions.getFIR(i).call()
            firs.append({
                "name": fir[0],
                "description": fir[1],
                "ipfs": fir[2],
                "timestamp": fir[3],
            })

        return render(request, "fir/template/view_fir.html", {"firs": firs})
