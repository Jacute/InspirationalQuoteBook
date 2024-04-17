async function getCategorieBlock(quotes) {
    const quotesList = document.getElementById('quotes');
    
    quotesList.innerHTML = '';

    quotes.forEach(quote => {
        const quoteCard = document.createElement('div');
        quoteCard.classList.add('block-quote');

        const quoteDic = document.createElement('div');
        quoteDic.classList.add('quote-dic');

        const quoteCat = document.createElement('div');
        quoteCat.classList.add('quote-cat');

        const quoteElement = document.createElement('h2');
        quoteElement.classList.add('quote');
        quoteElement.textContent = quote.quote;


        const author = document.createElement('p');
        author.classList.add('author');
        author.textContent = quote.quote_author;

        quoteCat.appendChild(quoteElement);
        quoteCat.appendChild(author);

        const categorieBlock = document.createElement('div');
        categorieBlock.classList.add('horizontal-block1');
        
        let categories = quote.categories.map(elem => upperFirstLetter(elem));
        categories.forEach(categorie => {
            const span = document.createElement('span');
            span.classList.add('categor');
            span.textContent = categorie;
            categorieBlock.appendChild(span);
        });

        // const quoteDelimiter = document.createElement('div');
        // quoteDelimiter.classList.add('line');

        quoteDic.appendChild(quoteCat);
        quoteDic.appendChild(categorieBlock);
        // quoteCardBody.appendChild(quoteDelimiter);

        quoteCard.appendChild(quoteDic);

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