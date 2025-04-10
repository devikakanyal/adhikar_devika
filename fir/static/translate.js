// Initialize Google Translate API
function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        { pageLanguage: 'en', includedLanguages: 'hi,ta,bn,pa', autoDisplay: false },
        'google_translate_element'
    );
}

// Toggle Language Dropdown Visibility
function toggleTranslateMenu() {
    let translateDiv = document.getElementById("google_translate_element");
    translateDiv.style.display = translateDiv.style.display === "none" ? "block" : "none";
}

// Load Google Translate Script Dynamically
let script = document.createElement("script");
script.type = "text/javascript";
script.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
document.body.appendChild(script);