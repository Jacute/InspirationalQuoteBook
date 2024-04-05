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
