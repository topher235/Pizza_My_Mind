var egg = new Egg();
egg
    .addCode("up,up,down,down,left,right,left,right,b,a", function () {
        // $('#egggif').fadeIn(500, function () {
        //     window.setTimeout(function () {
        //         $('#egggif').hide();
        //     }, 5000);
        // });
        document.getElementById('egggif').style.visibility = "visible";

    })
    .addHook(function () {
        console.log("Hook called for: " + this.activeEgg.keys);
        console.log(this.activeEgg.metadata);
    }).listen();
