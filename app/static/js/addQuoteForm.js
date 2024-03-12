var categories = [];
const category_list = document.getElementById('category_list');
const category_input = document.getElementById('category');


async function addCategory() {
    const category = category_input.value.trim();

    if (category) {
        categories.push(category);
        updateCategoryList();
        category_input.value = '';
    }
}

async function removeCategory(index) {
    categories.splice(index, 1);
    updateCategoryList();
}

async function updateCategoryList() {
    category_list.innerHTML = '';

    categories.forEach((category, index) => {
        const listItem = document.createElement('div');
        listItem.className = 'alert alert-custom alert-dismissible fade show mt-3';
        listItem.role = 'alert';

        const textItem = document.createTextNode(category);
        const closeButton = document.createElement('button');

        closeButton.type = 'button';
        closeButton.className = 'btn-close';
        closeButton.addEventListener('click', () => removeCategory(index));

        listItem.appendChild(textItem);
        listItem.appendChild(closeButton);

        category_list.appendChild(listItem);
    });
}


const form = document.getElementById("addQuote");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const errorsList = document.getElementsByClassName("errors-list")[0].querySelector('ul');
    const result = document.getElementById("result");
    const quote = document.getElementById("quote");
    const author = document.getElementById("quoteAuthor");

    result.classList.remove('show');
    result.innerHTML = "";
    errorsList.innerHTML = "";

    

    const queryResult = await addQuote(quote.value, author.value, categories);
    console.log(queryResult);
    if (queryResult['status'] === "OK") {
        const element = document.createElement('li');
        const result = document.getElementById("result");

        element.textContent = 'Ваша цитата успешно отправлена на модерацию';
        
        result.appendChild(element);
        
        result.classList.add('show');

    } else if (queryResult['status'] === 'BAD') {
        queryResult['errors'].forEach(error => {
            const element = document.createElement('li');
            const errorsList = document.getElementsByClassName("errors-list")[0].querySelector('ul');

            element.textContent = error;

            errorsList.appendChild(element);
        });
    }

    quote.value = '';
    author.value = '';
    category_list.innerHTML = '';
    categories = [];
});
