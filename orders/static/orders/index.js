window.addEventListener('popstate', function(event){

    if(event.state.code === -1){
        home_page();
    }
});

history.replaceState({code:null}, '', './' );

document.addEventListener('DOMContentLoaded', function() {
    
    history.pushState ({code:-1}, null, 'products');
    
    document.querySelector('#edit-view').style.display = 'none';
    // edit or delete button click handler
    document.querySelector("#products-view").onclick = (event) => {
        if(event.target.hasAttribute("data-code")){

            history.pushState ({code:0}, null, 'products');
            if(event.target.name==="edit"){
                edit_product(event.target.dataset.code);
            }
            else if(event.target.name==="delete"){
                // using setTimeout to run this function asynchronously 
                setTimeout(function() {
                    if (confirm(`Are you sure you want to delete the product?`)===true){
                        fetch(`api/v1/product/${event.target.dataset.pk}`, {
                            method:'DELETE'
                        })
                        .then(res => {
                            if(res.status===204){
                                location.reload();
                            }
                        });
                    }else{
                        console.log("cancel");
                    }
                });
                
                
            }
            
        }
    };  
    // add product button handler
    document.querySelector("#create-button").onclick = () => {
        history.pushState ({code:0}, null, 'products');
        create_product();
    };
    // handler for both add product and edit product
    document.querySelector("#compose-form").onsubmit = (event) => {

        var form_data = {};

        //variable to decide weather to edit or add new product
        let edit = false;

        // getting the form data
        event.target.childNodes.forEach(node =>{
            if(node.name){
                form_data[node.name] = node.value;
            }
            if(node.disabled){
                edit = true;
            }
        });
        form_data["row_status"] = 1;

        if (edit){
            fetch('api/v1/product/', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'product-code':form_data['product_code']
            },
            body:JSON.stringify(form_data)
            })
            .then(res => {
                if(res.status===204){
                    location.reload();
                } else if (res.status===400) {
                	res.json().then(err => {
                	    alert(`${Object.keys(err)[0]}: ${err[Object.keys(err)[0]][0]}`);	
                	});
                }
            });
        } else{
            fetch('api/v1/product/create', {
                method:'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify(form_data)
            })
            .then(res => {
                if(res.status===201){
                    location.reload();
                } else if (res.status===400) {
                	res.json().then(err => {
                	    alert(`${Object.keys(err)[0]}: ${err[Object.keys(err)[0]][0]}`);	
                	});
                }
            });
        }
        return false;
    };
    // navigate to order page
    document.querySelector("#order-page").onclick = () => {
        window.location.href = "order";
    };

  });

  
  function home_page(){
    document.querySelector('#products-view').style.display = 'block';
    document.querySelector('#create-product').style.display = 'block';
    document.querySelector('#edit-view').style.display = 'none';
  }

  function create_product(){
    
    document.querySelector('#products-view').style.display = 'none';
    document.querySelector('#create-product').style.display = 'none';
    document.querySelector('#edit-view').style.display = 'flex';
    // reset the form fields
    document.querySelectorAll("#compose-form input").forEach(node => {
        if (node.disabled){
            node.disabled = false;
        }
        if (node.id!="submit-form"){
            node.value = "";
        }
        
    });
    
  }

  function edit_product(code) {
    document.querySelector('#products-view').style.display = 'none';
    document.querySelector('#create-product').style.display = 'none';
    document.querySelector('#edit-view').style.display = 'flex';
    // prepopulate the product details
    fetch(`api/v1/product/`, {
        headers:{
            'product-code':code,
        }
    })
    .then(response => response.json())
    .then(
        product => {
            document.querySelectorAll('input').forEach(data => {
                if (data.name){
                    data.value = product[data.name];
                }
            });
    });
    // disable everything but editable fields
    document.querySelectorAll("#compose-form input").forEach(node => {
        if( !node.disabled && !(node.name=="unit_price" || node.name=="current_stock" || node.id=="submit-form") ){
            node.disabled = true;
        }
    });

  }