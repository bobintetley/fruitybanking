/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, SHOW_VAT, descs, desctoaccount */

function trx_onload() {

    // Called when the transaction viewing page is loaded

    // Bind datepickers and jquery button to the date range at the top
    $("#datefrom, #dateto").datepicker({ dateFormat: "dd/mm/yy" });
    $("#filterdate").button();

    // Autocomplete from previous transaction descriptions, when one is
    // picked automatically choose the last account we saw for it
    $("input[name='description']").autocomplete({ source: descs }).blur(function() {
        var oa = desctoaccount[$(this).val()];
        if (oa) {
            $("select[name='otheraccount']").val(oa);
        }
    });

    // Hide any vat controls if show vat is off
    if (!SHOW_VAT) { $(".showvat").hide(); }

    // When reconcile is clicked, process it asynchronously and update 
    // the element to show reconciled
    $(".reconcile-link").on("click", function() {
        var tid = $(this).attr("data-trx-id"),
            cell = $(this).closest(".reconciled");
        $.ajax({
            type: "GET",
            url: "transaction_reconcile",
            data: { "id": tid },
            cache: false,
            dataType: "text",
            mimeType: "textPlain"
        }).then(function(r) {
            if (r == "OK") { cell.html("R"); }
        });
        return false; // cancel the click
    });

    // When vat is clicked, process it asynchronously and update 
    // the element to show reconciled
    $(".vat-link").on("click", function() {
        var tid = $(this).attr("data-trx-id"),
            cell = $(this).closest(".vat");
        $.ajax({
            type: "GET",
            url: "transaction_vat",
            data: { "id": tid },
            cache: false,
            dataType: "text",
            mimeType: "textPlain"
        }).then(function(r) {
            if (r == "OK") { cell.html("V"); }
        });
        return false; // cancel the click
    });


    // Scroll to the bottom of the screen and focus the new trx/date field
    window.scrollTo(0, document.body.scrollHeight);
    $("#datebox").focus();

}


