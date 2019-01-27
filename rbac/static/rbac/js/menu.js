$('.multi-menu .title').click(function () {
    console.log("触发了");
    $(this).next().toggleClass('hide');
});
