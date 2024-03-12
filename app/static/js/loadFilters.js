async function loadModalAuthors(authors, selectedAuthor) {
    authorsDropdown.innerHTML = '';

    let all = document.createElement('option');
    all.text = 'Все';
    all.setAttribute('value', '');
    authorsDropdown.add(all);

    authors.forEach(author => {
        let option = document.createElement('option');
        option.text = upperFirstLetter(author);
        option.setAttribute('value', upperFirstLetter(author));
        
        authorsDropdown.add(option);
    });

    if (selectedAuthor) {
        authorsDropdown.value = selectedAuthor;
    }
}

async function loadModalCategories(categories, selectedCategory) {
    categoriesDropdown.innerHTML = '';

    let all = document.createElement('option');
    all.text = 'Все';
    all.setAttribute('value', '');
    categoriesDropdown.add(all);

    categories.forEach(categorie => {
        let option = document.createElement('option');
        option.text = upperFirstLetter(categorie);
        option.setAttribute('value', upperFirstLetter(categorie));

        categoriesDropdown.add(option);
    });

    if (selectedCategory) {
        categoriesDropdown.value = selectedCategory;
    }
}

function loadFilters() {
    const filters = {};

    const inputElement = document.getElementById('query');
    const authorsDropdown = document.getElementById('authorsDropdown');
    const categoriesDropdown = document.getElementById('categoriesDropdown');
    
    const selectedAuthorOption = authorsDropdown.options[authorsDropdown.selectedIndex];
    const selectedCategoryOption = categoriesDropdown.options[categoriesDropdown.selectedIndex];

    filters.author = selectedAuthorOption.value;
    filters.categorie = selectedCategoryOption.value;
    filters.query = inputElement.value;

    return filters;
}


getAuthors('').then((response1) => { // Загрузка данных в модель
    getCategories('').then((response2) => {
        let authors = response1.data;
        let categories = response2.data;

        loadModalAuthors(authors);
        loadModalCategories(categories);
    })
});
