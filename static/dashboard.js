const a = document.querySelectorAll('.nocycles');

if(a[0] !== undefined) {
    a[0].addEventListener('click', () => {
        alert('Your limit has been reached, pls contact adminstration to add more cycles')
    })
    
    a[1].addEventListener('click', () => {
        alert('Your limit has been reached, pls contact adminstration to add more cycles')
    })
}