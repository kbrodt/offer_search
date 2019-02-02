$(document).ready(function(){
	$('#last-item').on('click', '.go_to_href', function(){
		location.href = $(this).attr('href');
	});
	
	$('#search_button').on('click', function(){
		if($('#search_input').val().length > 0){
			$.ajax({
				type : 'POST',
				data: {data: $('#search_input').val()},
				url: "py/search.py",
				dataType: 'text',
				success: function(data){
					my_json = JSON.parse(data.replace(/\"/g, '')
					.replace(/\'/g, '"')
					.replace(/\n/g, "")
					.replace(/\r/g, "")
					.replace(/\t/g, "")
					.replace(/\f/g, ""));
					//console.log(my_json);
					$('#all_items_block').empty();
					for(var i=0; i < my_json.length; i++)
					{
						all_products = '<p>';
						for(var j=0; j < my_json[i]['products'].length; j++)
							all_products += '<b>Путь к товару:</b> ' + my_json[i]['products'][j].Item + '</br>' +
											'<b>Описание товара:</b> ' + my_json[i]['products'][j].Attributes + '</br>' +
											'<b>Цена:</b> ' + my_json[i]['products'][j].Price + '</br></br>';
						all_products += '</p>';
						all_products.replace('\~', ' ');
						$('#all_items_block').append('<div class="col-xs-12 accordion" style="cursor: pointer;"><a class="item-block"><header><img src="assets/img/Tinkoff-bank.png" alt=""><div class="hgroup" style="display: inline;"><h4 href="' + my_json[i]['offer'].web +'" class="go_to_href">' + my_json[i]['offer'].offer +'</h4><h5>' + my_json[i]['offer'].advert_text + '</h5></div><div class="header-meta" style="position: absolute; top: 14px; right: 37px;"><span class="location">КБ '+ my_json[i]['offer'].cashback +'%</span><span class="label label-success">' + my_json[i]['offer'].period + ' месяцев</span></div></header></a></div><div class="panel" style="margin-left: 40px; margin-right: 40px;">'+ all_products +'</div>');
					}
					var acc = $(".accordion");
					var i;

					for (i = 0; i < acc.length; i++) {
					  acc[i].addEventListener("click", function() {
						this.classList.toggle("active");

						var panel = this.nextElementSibling;
						if (panel.style.display === "block") {
						  panel.style.display = "none";
						} else {
						  panel.style.display = "block";
						}
					  });
					}
					
					$('html, body').animate({ scrollTop: $('#last-item').offset().top + 300 }, 500);
				},
				error: function(e){
					console.log(e);
					console.log('Ошибка')
				}
			});
		}
	});
});