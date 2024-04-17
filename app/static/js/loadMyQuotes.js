async function getCategorieBlock(quotes) {
    const myQuoteContainer = document.getElementById('myQuoteContainer');
    
    quotes.forEach(quote => {
        const quoteCard = document.createElement('div');
        quoteCard.classList.add('block-quote');

        const quoteDic = document.createElement('div');
        quoteDic.classList.add('my_quote-dic');

        const quoteDic2 = document.createElement('div');
        quoteDic2.classList.add('my_quote-dic2');
        quoteDic2.id = 'quotes';

        const quoteElement = document.createElement('h2');
        quoteElement.classList.add('my_quote-quote');
        quoteElement.textContent = quote.quote;


        const author = document.createElement('p');
        author.classList.add('my_quote-author');
        author.textContent = quote.quote_author;

        quoteDic2.appendChild(quoteElement);
        quoteDic2.appendChild(author);

        const categorieBlock = document.createElement('div');
        categorieBlock.classList.add('horizontal-block1');
        
        let categories = quote.categories.map(elem => upperFirstLetter(elem));
        categories.forEach(categorie => {
            const span = document.createElement('span');
            span.classList.add('categor');
            span.textContent = categorie;
            categorieBlock.appendChild(span);
        });

        quoteDic2.appendChild(categorieBlock);

        const statusContainer = document.createElement('div');
        statusContainer.classList.add('aaa');

        const status = document.createElement('p');
        if (quote.status == '1') {
            status.classList.add('status-complete');
            status.textContent = 'Опубликована';
        } else if (quote.status == '2') {
            status.classList.add('status-under-consideration')
            status.textContent = 'На модерации';
        } else {
            status.classList.add('status-ban');
            status.textContent = 'Отклонена';
        }
        statusContainer.appendChild(status);

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete');
        deleteButton.id = 'delete-button-quote';
        deleteButton.textContent = 'Удалить';
        statusContainer.appendChild(deleteButton);

        quoteDic.appendChild(quoteDic2);
        quoteDic.appendChild(statusContainer);
        quoteCard.appendChild(quoteDic);
        myQuoteContainer.appendChild(quoteCard);

        
    });

}

async function myQuotes() {
    const response = await getMyQuotes();
    console.log(response);
    getCategorieBlock(response.data);
}

myQuotes();