function next(name, offset) {
    js_offsets[name] += offset;
    if (js_offsets[name] < 0) {
        js_offsets[name] = 0;
    }
    if (js_offsets[name] >= js_comics[name].length) {
        js_offsets[name] = js_comics[name].length - 1;
    }
    return js_offsets[name];
}

function init() {
    // key = foreach js_comic
    // key uses json to set src
}

function handle_swap(self, offset) {
    $(self).on("click", function() {
      let group_url = $(self)
        .parent()
        .find(".comicUrl")
        .attr("href");

      let $image = $(self)
        .parent()
        .find(".comicImage");

      let $title = $(self)
        .parent()
        .find(".comicTitle");

      // let group_url = $title.attr('href');
      let i = next(group_url, offset);
      let new_title = js_comics[group_url][i]['comic_title'];
      $title.html(new_title);

      console.log(group_url, i, new_title);
      // console.log(title);
    });

}

$(document).ready(function() {

  $('.prevButton').each(function(index, value) {
      let self = this;
      $(self).on("click", function() {

          let group_url = $(self)
              .parent()
              .find(".comicUrl")
              .attr("href");

          let $image = $(self)
              .parent()
              .find(".comicImage");

          let $title = $(self)
              .parent()
              .find(".comicTitle");

          // let group_url = $title.attr('href');
          let i = next(group_url, 1);
          let new_title = js_comics[group_url][i]['comic_title'];
          let new_src = js_comics[group_url][i]['image_src'];

          $title.html(new_title);
          $image.attr('src', new_src);
      });
  });

  $('.nextButton').each(function(index, value) {
    let self = this;
    $(self).on("click", function() {

      let group_url = $(self)
        .parent()
        .find(".comicUrl")
        .attr("href");

      let $image = $(self)
        .parent()
        .find(".comicImage");

      let $title = $(self)
        .parent()
        .find(".comicTitle");

      // let group_url = $title.attr('href');
      let i = next(group_url, -1);
      let new_title = js_comics[group_url][i]['comic_title'];
      let new_src = js_comics[group_url][i]['image_src'];

      $title.html(new_title);
      $image.attr('src', new_src);

      console.log(group_url, i, new_title);
      // console.log(title);
    });
  });

});