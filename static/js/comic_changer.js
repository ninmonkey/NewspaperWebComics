// comics = {
//     "xkcd.com": [
//       {
//         src: "509916.png",
//         title: "SafetySat",
//       },
//       {
//         src: "509916.png",
//         title: "driving cars",
//       }
//     ]
// };

// offsets = {
//     "xkcd.com": 0,
// };
function next(name) {
    offsets[name] += 1;
    if (offsets[name] < 0) {
        offsets[name] = 0;
    }
    if (offsets[name] >= comics[name].length) {
        console.log('too far dude');
        offsets[name] = comics[name].length - 1;
    }
    console.log("i=", offsets[name]);
    off = offsets[name];
    return {
        title: comics[name][off].title
    };
}

function prev(name) {
    off = offsets[name];
    off -= 1;

    if (offsets[name] <= 0) {
        offsets[name] = 0;
    }
    console.log("i=", offsets[name]);

    return {
        title: comics[name][off].title
    };
}

function init() {
  // key = foreach js_comic
  // key uses json to set src
}

$( document ).ready(function() {

    return;
    $("#title").html(comics['xkcd.com'][0].title);

    $("#image").on("click", function() {
        console.log('click');
        //$("#title").html(comics['xkcd.com'][1].title);
        ret = next('xkcd.com');
        $("#title").html(ret.title);
    });

    $("#title").on("click", function() {
        console.log('click');
        //$("#title").html(comics['xkcd.com'][1].title);
        ret = prev('xkcd.com');
        $("#title").html(ret.title);
    });
});