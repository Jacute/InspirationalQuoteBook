async function getCategories(author) {
    try {
        const response = await fetch(`/api/get/quotes/categories?author=${author}`);
        const result = JSON.parse(await response.text());

        return result;

    } catch (error) {
        console.error(error);
    }
}

async function getAuthors(categorie) {
    try {
        const response = await fetch(`/api/get/quotes/authors?category=${categorie.toLowerCase()}`);
        const result = JSON.parse(await response.text());

        return result;
    } catch (error) {
        console.error(error);
    }
}

async function getQuotes(author, categorie, query) {
   try {
        const response = await fetch(`/api/get/quotes/query?author=${author}&category=${categorie.toLowerCase()}&query=${query.toLowerCase()}`);
        const result = JSON.parse(await response.text());

        return result;
   } catch (error) {
        console.error(error);
   } 
}

async function getMyQuotes() {
    try {
        const response = await fetch('/api/get/quotes/my');
        const result = JSON.parse(await response.text());

        return result;
    } catch (error) {
        console.error(error);
    }
}

async function addQuote(quote, author, categories) {
    const data = {
        quote: quote,
        author: author,
        categories: categories
    };
    try {
        const response = await fetch('/api/put/quotes/', {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data) 
        });
        const result = await response.json();
        
        return result;
    } catch (error) {
        console.error(error);
    }
}

// удаление цитаты

// const deleteButton = document.querySelector("button[data-block-id='quote']");

// deleteButton.addEventListener("click", async () => {
//   const response = await fetch("/api/delete-block", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ blockId: "quote" }),
//   });

//   const data = await response.json();

//   if (data.success) {
//     // Удалить блок из DOM
//     const block = document.getElementById("quote");
//     block.parentNode.removeChild(block);
//   } else {
//     // Отобразить сообщение об ошибке
//     alert("Не удалось удалить блок. Повторите попытку.");
//   }
// });