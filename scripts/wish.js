// API


$(document).ready(function () {
show_wish();
});

function show_wish() {
$.ajax({
    type: "GET",
    url: "/wish",
    data: {},
    success: function (response) {
        let rows = response['wish']
        for(let i = 0; i <rows.length; i++) {
            let todo = rows[i].wish
            let temp_html = `<li>
                                <input className="check" type="checkbox" name="interest"/>
                                <h4>${todo}</h4>
                            </li>`

            $('#wish-list').append(temp_html)
        }

    alert(response["msg"]);
    },
});
}

function save_wish() {
    let wish = $('#wish').val()
$.ajax({
    type: "POST",
    url: "/wish",
    data: { wish_give: wish},
    success: function (response) {
    alert(response["msg"]);
    window.location.reload();
    },
});
}

// function done_wish(num) {
// $.ajax({
//     type: "POST",
//     url: "/wish/done",
//     data: { wish_give: num },
//     success: function (response) {
//     alert(response["소원 성취!"]);
//     },
// });
// }




//친구 트리 놀러가기 버튼 누르면 다른 페이지로 이동하는 기능
function toOthers() {
  window.location.href = "sample.html";
}
