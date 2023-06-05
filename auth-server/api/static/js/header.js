;
(function($, window, document) {
    "use strict";

    function responsiveMenu() {
        var mobW = $(".site-header").attr("data-mobile-menu-resolution");

        if (window.outerWidth < mobW || $(".site-header").hasClass(".mobile-header")) {
            if (!$(".site-header .has-submenu i").length) {
                $(".site-header .has-submenu").append('<i class="feather-plus"></i>');
                $(".site-header .has-submenu i").addClass("hide-drop");
            }

            $(".site-header .has-submenu i").on("click", function() {
                if (!$(this).hasClass("animation")) {
                    $(this).parent().toggleClass("is-open");
                    $(this).addClass("animation");
                    $(this).parent().siblings().removeClass("is-open").find(".feather-plus").removeClass("hide-drop").prev(".sub-menu").slideUp(200);
                    if ($(this).hasClass("hide-drop")) {
                        if ($(this).closest(".sub-menu").length) {
                            $(this).removeClass("hide-drop").prev(".sub-menu").slideToggle(200);
                        } else {
                            $(".site-header .has-submenu i").addClass("hide-drop").next(".sub-menu").hide(200);
                            $(this).removeClass("hide-drop").prev(".sub-menu").slideToggle(200)
                        }
                    } else {
                        $(this).addClass("hide-drop").prev(".sub-menu").hide(100).find(".site-header .has-submenu a").addClass("hide-drop").prev(".sub-menu").hide(200)
                    }
                }

                setTimeout(removeClass, 250);

                function removeClass() {
                    $(".site-header .has-submenu i").removeClass("animation")
                }

            })
        } else {
            $(".site-header .has-submenu i").remove()
        }
    }



    $(window).on("load resize", function() {
        responsiveMenu();
    });

    // window.addEventListener("orientationchange", function() {
    // 	responsiveMenu()
    // });
})(jQuery, window, document);