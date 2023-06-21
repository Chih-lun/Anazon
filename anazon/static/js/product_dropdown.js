$.ajax({
    type: "GET",
    url: '/get_categories',
    dataType: "json",
    success: function (response) {
        // display categories on nav dropdown
        categories = response.categories;
        var dropDown = $("#product_dropdown");
        dropDown.append(`<a class="dropdown-item" href="/product/">All</a>`)
        for (var i=0; i<categories.length; i++){
            dropDown.append(`<a class="dropdown-item" href="/product/?category=${categories[i]}">${categories[i]}</a>`);
        }
    },
    error: function (thrownError) {
      console.log(thrownError);
    }
  });

