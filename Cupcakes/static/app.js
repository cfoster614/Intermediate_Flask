async function addCupcakeToDatabase(flavor, size, rating, image, id) {
    resp = await axios.post('/api/cupcakes', {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    })
    return postNewCupcake(id);
}

async function postNewCupcake(id){
    resp = await axios.get(`api/cupcakes/${id}`);
    data = resp.data.cupcake;
    console.log(data.image);
    $('tbody').append($('<tr>', {id : `cupcake-${id}`}));

    $(`#cupcake-${id}`).append($('<td>', {id : `img-${id}`}));
    $(`#img-${id}`).append($('<img>', {src: data.image}));
    $(`#cupcake-${id}`).append($('<td>').text(data.flavor));
    $(`#cupcake-${id}`).append($('<td>').text(data.size));
    $(`#cupcake-${id}`).append($('<td>').text(data.rating));
}



function getFormData(e) {
    e.preventDefault();
    const id = Number($('#hidden').val()) + 1;
    const flavor = $('#flavor-input').val();
    const size = $('#size-input').val();
    const  rating = $('#rating-input').val();
    let image = $('#image-input').val();

    if (!image) {
        image = 'https://cdn.pixabay.com/photo/2017/05/04/21/23/cupcakes-2285209_1280.jpg';
    }
   
    return addCupcakeToDatabase(flavor, size, rating, image, id);
    
}



$('form').submit(getFormData);

$('input[type=range]').on('input', function(){
    value = $('input[type=range]').val()
    $('.range-label').text(`${value} stars`)
});