var book_app = angular.module('bookApp',[]);

book_app.controller('bookController', function($scope, $http, $compile){
	$scope.bookList = null;
	$scope.addQuantity = 0;
	
	$scope.getBookList = function(type){
		//original page type=null
		if (type == null){
			type = "nil";
			document.getElementById("leftbar").style.display="none";
			document.getElementById("footer").style.display="none";
			document.getElementById("contentArea").style.display="none";
			document.getElementById("cartSummary").style.display="none";
		}
		
	};
	
	$scope.getBookInformation = function(id){
		var bookid = id;
		
		$http.get("/myroutes/loadbook/"+bookid).then( function(response){
			$scope.information = response.data[0];
		//	var picture = $compile("<div class='infoPic' id='infoPic1'><img ng-src='{{information.coverImage}}' class='infoCover' height='420' width='280'></div>")($scope);
			angular.element(document.getElementById("leftbar")).css('background','none');
		//	angular.element(document.getElementById("firstbox")).after(picture);
			document.getElementById("infoPic1").style.display="grid";
			document.getElementById("firstbox").style.display="none";
			document.getElementById("secondbox").style.display="none";
			document.getElementById("thirdbox").style.display="none";
			document.getElementById("footer").style.display="none";
			var description = $compile("<table id='inforTable'><tri><td width='50%'><div class='informationLayout'><div><ul><li>{{information.title}}</li><li>{{information.authorList}}</li><li>{{information.price}}</li><li>{{information.publisher}}</li><li>{{information.date}}</li><li>{{information.description}}</li></ul></div></td><td class='CartBox_InfoPage'><p>Quantity: <input id='addQuantity' type='number' max='99' ng-model='addQuantity'></input><p><button class={{information._id}} id='addBookBtn' ng-click='addToCart()'>Add to Cart</button></td></tr><tr><td ng-click='back1()'>GO BACK</td></tr></table>")($scope);
			angular.element(document.getElementById("contentLayout")).after(description);
			document.getElementById("contentLayout").style.display = "none";
			document.getElementById("pagenav").style.display = "none";
		}, function (response){
			alert("Error: " + response.statusText);
		});
	};
	
	$scope.back1 = function(){
		document.getElementById("infoPic1").style.display="none";	
		angular.element(document.getElementById("leftbar")).css('background','red');
		document.getElementById("firstbox").style.display="grid";
		document.getElementById("secondbox").style.display="grid";
		document.getElementById("thirdbox").style.display="grid";
		document.getElementById("inforTable").style.display = "none";
		document.getElementById("contentLayout").style.display = "grid";
		document.getElementById("pagenav").style.display = "inline";
		document.getElementById("addedPage").style.display = "none";
	}
	
	$scope.back2 = function(){
		document.getElementById("contentLayout").style.display = "grid";
		$http.get('/myroutes/loadpage', {params: {category: 'nil'}}).then( function(response){
			$scope.bookList = response.data;
			for (var i=0; i<$scope.bookList.length; i++){
				var book = ($scope.bookList)[i];
			}
		}, function (response){
			alert("Error: " + response.statusText);
		});		
		angular.element(document.getElementById("leftbar")).css('background','red');
					document.getElementById("infoPic1").style.display="none";
		document.getElementById("firstbox").style.display="grid";
		document.getElementById("secondbox").style.display="grid";
		document.getElementById("thirdbox").style.display="grid";
		document.getElementById("inforTable").style.display = "none";
		document.getElementById("pagenav").style.display = "inline";
		document.getElementById("addedPage").style.display = "none";
		document.getElementById("paidPage").style.display = "none";
	}
	
	$scope.loginPage = function(){
		document.getElementById("mainPage").style.display="none";
		document.getElementById("footer").style.display="none";
		document.getElementById("login").style.display="inline";	
		document.getElementById("infoPic1").style.display="none";
	}
	
	$scope.signin = function(user) {
		if ( ($scope.name != null) && ($scope.password != null) ) {
			$http.post('/myroutes/signin', {name: $scope.name, password: $scope.password}).then(function(response) {		
				if(response.data == 'login failure'){
					alert("Error");
				}else{
				$scope.msg =response.data;
				$scope.loginname = $scope.msg.name;
				$scope.cartnum = $scope.msg.totalnum;
				var description = $compile("<td width='85%' id='firstCell'><div id='xxx'>Hello {{loginname}} <a href='#' id='signoutbtn' ng-click='signout()'>(Sign out)</a></div></td>")($scope);
				angular.element(document.getElementById("firstCell")).replaceWith(description);
				document.getElementById("mainPage").style.display="inline";
				document.getElementById("footer").style.display="inline";
				document.getElementById("login").style.display="none";
				document.getElementById("cartBtn").style.display="inline";
				document.getElementById("cartmsg").style.display="inline";
				}
		}, function(response){
			alert("Error:" + response.statusText);
		});
		$scope.name=null;
		$scope.password=null;
		} else {
			alert("You must enter username and password");
			$scope.name=null;
			$scope.password=null;
		}
	}
	
	$scope.register = function(){
		document.getElementById("signin_btn").style.display="none";
		document.getElementById("register_btn").style.display="none";
		document.getElementById("email_row").style.display="table-row";
		document.getElementById("token_row").style.display="table-row";
		document.getElementById("send_token_btn").style.display="inline";
		document.getElementById("role_row").style.display="table-row";
		document.getElementById("submit_btn").style.display="table-row";
	}
	
	$scope.signout = function(){
		$http.get('/myroutes/signout').then( function(response){
			if(response.data == ''){
				var signoutmsg = $compile("<td width='85%' id='firstCell'><a href='#' ng-click='loginPage()' class='typicalBtn' id='signinbtn'>Sign in</a></td>")($scope);
				angular.element(document.getElementById("firstCell")).replaceWith(signoutmsg);
				document.getElementById("cartBtn").style.display="none";
				document.getElementById("cartmsg").style.display="none";
			}else{
				alert("Error:" + response.data.msg);
			}
		}, function(response){
			alert("Error:" + response.statusText);
		});
	}
	
	$scope.addToCart = function(){
		$scope.amount = null;
		$scope.numberOfBooks = 0;
		var bookId = document.getElementById('addBookBtn').getAttribute('class');
		$http.put('/myroutes/addtocart', {bookId: bookId, quantity: $scope.addQuantity}).then(function(response){
				if(response.statusText == 'OK'){
					$scope.numberOfBooks = response.data.totalnum;
					$scope.amount = response.data.total_price;
					$scope.cartnum = response.data.totalnum;
					document.getElementById("inforTable").style.display = "none";
					document.getElementById("addedPage").style.display = "inline";
				}else{
					alert("Error:" + response.statusText);
				}
		}, function(response){
			alert("Error:" + response.statusText);
		});
	}
	
	//load cart content when the cart area is clicked
	$scope.loadCart = function(){
		$http.get('/myroutes/loadcart').then( function(response){
				if(response.statusText == 'OK'){
					$scope.cartList = response.data;
					$scope.subtotal = 0;
					$scope.totalCount = 0;
					for(var i=0; i<$scope.cartList.length; i++){
						var order = ($scope.cartList)[i];
						$scope.totalCount += $scope.cartList[i].quantity;
						$scope.subtotal += $scope.cartList[i].quantity * $scope.cartList[i].price.replace('$','');
					}
					document.getElementById("infoPic1").style.display="none";
					document.getElementById("cartSummary").style.display = "inline";	
					document.getElementById("shoppingCart").style.display = "inline";	
					document.getElementById("contentArea").style.display = "none";					
					document.getElementById("firstbox").style.display = "none";
					document.getElementById("secondbox").style.display = "none";
					document.getElementById("thirdbox").style.display = "none";
					document.getElementById("footer").style.display = "none";
					document.getElementById("contentLayout").style.display = "none";
					document.getElementById("addedPage").style.display = "none";
					document.getElementById("pagenav").style.display = "none";	
				}else{
					alert("Error:" + response.statusText);
				}
		}, function (response){
			alert("Error:" + response.statusText);
		});
	}
	
	//Go to checkout page when the checkout button is clicked
	$scope.checkout = function(){
		$http.get('/myroutes/checkout/').then (function(response){
			if (response.data == ''){
					document.getElementById("summaryTitle").style.display = "none";							
					document.getElementById("cartSummary").style.display = "none";
					document.getElementById("firstbox").style.display = "none";
					document.getElementById("secondbox").style.display = "none";
					document.getElementById("thirdbox").style.display = "none";
					document.getElementById("footer").style.display = "none";
					document.getElementById("contentLayout").style.display = "none";
					document.getElementById("addedPage").style.display = "none";
					document.getElementById("pagenav").style.display = "none";	
					document.getElementById("paidPage").style.display = "inline";
					$scope.cartnum = 0;
			}
		}, function (response){
			alert('Erorr:' + response.statusText);
		});
	}
	
	//update the shopping cart
	$scope.updateCart = function(bookId, quantity){
		var tempList = [];
		var price =0;
		if (quantity == 0){
			$scope.deleteBook(bookId);
		}else{
			$http.put('/myroutes/updatecart',{'bookId': bookId, 'quantity': quantity}).then(function(response){
				if(response.statusText =='OK'){
					alert("OK");
					$scope.totalCount = response.data.totalnum;
					$scope.cartnum = response.data.totalnum;
					for(var i=0; i < $scope.cartList.length; i++){
						if ($scope.cartList[i]._id == bookId){
							$scope.cartList[i].quantity = quantity;
						}

					}
				
				for (var i=0; i< $scope.cartList.length; i++){
					price = price + $scope.cartList[i].price.replace('$','') * $scope.cartList[i].quantity;
				}
				$scope.subtotal = price;
				}
			});		
		}
	}
	
	
	//delete a book from the cart
	$scope.deleteBook = function(bookId){
		
		$http.put('/myroutes/deletefromcart/' + bookId).then(function(response){
			if(response.statusText == 'OK'){
				$scope.editedCount = response.data.totalnum;
				$scope.numberOfBooks = $scope.editedCount;
			}
			
		}, function(response){
			alert("Error:" + response.statusText);
		});
					
					/*
					for(var i=0; i<$scope.cartList.length; i++){
						var order = ($scope.cartList)[i];
						$scope.totalCount += $scope.cartList[i].quantity;
						$scope.subtotal += $scope.cartList[i].quantity * $scope.cartList[i].price.replace('$','');
					}	*/	
	}
	
	
});