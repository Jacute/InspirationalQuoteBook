async function getCategorieBlock(quotes) {
    const quotesList = document.getElementById('quotes');
    
    quotesList.innerHTML = '';

    quotes.forEach(quote => {
        const quoteCard = document.createElement('div');
        quoteCard.classList.add('block', 'border-bottom');
        quoteCard.classList.add('card', 'mb-3');

        const quoteCardBody = document.createElement('div');
        quoteCardBody.classList.add('card-body');

        const quoteText = document.createElement('p');
        quoteText.classList.add('card-text', 'quote-text');
        quoteText.innerText = quote.quote;

        const quoteAuthor = document.createElement('p');
        quoteAuthor.classList.add('card-text');
        quoteAuthor.innerHTML = `<strong>Автор:</strong> ${quote.quote_author}`;
        
        let categories = quote.categories.map(elem => upperFirstLetter(elem));
        const quoteCategory = document.createElement('p');
        quoteCategory.classList.add('card-text');
        quoteCategory.innerHTML = `<strong>Категории:</strong> ${categories.join(", ")}`;

        quoteCardBody.appendChild(quoteText);
        quoteCardBody.appendChild(quoteAuthor);
        quoteCardBody.appendChild(quoteCategory);

        quoteCard.appendChild(quoteCardBody);
        quotesList.appendChild(quoteCard);
    });

}

async function searchHandler() {
    const filters = loadFilters();

    const response = await getQuotes(filters.author, filters.categorie, filters.query);

    getCategorieBlock(response.data);
}

const inputElement = document.getElementById('query');
const searchButton = document.getElementById('search');

const authorsDropdown = document.getElementById('authorsDropdown');
const categoriesDropdown = document.getElementById('categoriesDropdown');

inputElement.addEventListener('keydown', function(event) {

    if (event.key === 'Enter') {
    event.preventDefault();
    searchHandler();
    
  }
});

searchButton.addEventListener('click', function() {
    searchHandler();
});

authorsDropdown.addEventListener("change", function() {
    const selectedCategoryOption = categoriesDropdown.options[categoriesDropdown.selectedIndex];
    const category = selectedCategoryOption.value;

    const selectedAuthorOption = authorsDropdown.options[authorsDropdown.selectedIndex];
    const author = selectedAuthorOption.value;
  
    getCategories(author).then(response => {
        loadModalCategories(response.data, category);
    });

    searchHandler();
});

categoriesDropdown.addEventListener("change", function() {
    const selectedCategoryOption = categoriesDropdown.options[categoriesDropdown.selectedIndex];
    const category = selectedCategoryOption.value;

    const selectedAuthorOption = authorsDropdown.options[authorsDropdown.selectedIndex];
    const author = selectedAuthorOption.value;

    getAuthors(category).then(response => {
        loadModalAuthors(response.data, author);
    });

    searchHandler();
});