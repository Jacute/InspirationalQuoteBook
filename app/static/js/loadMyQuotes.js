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

        const status = document.createElement('p');
        status.classList.add('card-text');
        if (quote.status == '1') {
            status.innerHTML = `<strong>Статус:</strong> <div style="color: green">Опубликована</div>`;
        } else if (quote.status == '2') {
            status.innerHTML = `<strong>Статус:</strong> <div style="color: yellow">На модерации</div>`;
        } else {
            status.innerHTML = `<strong>Статус:</strong> <div style="color: red">Отклонена</div>`;
        }

        quoteCardBody.appendChild(quoteText);
        quoteCardBody.appendChild(quoteAuthor);
        quoteCardBody.appendChild(quoteCategory);
        quoteCardBody.appendChild(status);


        quoteCard.appendChild(quoteCardBody);
        quotesList.appendChild(quoteCard);
    });

}

async function myQuotes() {
    const response = await getMyQuotes();

    getCategorieBlock(response.data);
}

myQuotes();