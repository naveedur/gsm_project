console.log("this is js file to integrate payment gateway")

const tokenizationSpecification={
    type:PAYMENT_GATEWAY,
    parameters:{
        gateway:'example',
        gatewayMerchantId:"gatewayMerchantId" 
    },
}

const cardPaymentMethod={
    type:'CARD',
    tokenizationSpecification:tokenizationSpecification,
    parameters:{
        allowedCardNetwroks: ['VISA', 'MASTERCARD'],
        allowedAuthMethods: ['PAN-ONLY','CRYPTOGRAM_3DS']

    },
}

const googlePayConfiguration={
    apiVersion:2,
    apiVersionMinor: 0,
    allowedPaymentMethods:[cardPaymentMethod]
}





let googlePayClient
console.log("ssss")
function onGooglePayLoaded(){
    // console.log("another console in js")
    console.log("onload function is run ")
    googlePayClient = new google.payments.api.PaymentsClient({environment: 'TEST'});
    googlePayClient.isReadyToPay(googlePayConfiguration)
    .then(response=>{
        if(response.result){
            createAndAddButton();
        }
        else{
            // current user can not pay with google pay. Try another payment method
        }
    })
    .catch(error=> console.error("isReadyTOPay: ", error))
}

function createAndAddButton(){
    const googlePayButton= googlePayClient.createButton({
        onclick: onGooglePayButtonCLicked
    })
    document.getElementById('buy_now').appendChild(googlePayButton);

}

function onGooglePayButtonCLicked(){
    const paymentDataRequest= {...googlePayConfiguration}
    paymentDataRequest.merchantInfo={
        merchantId:'BCR2DN4TQC7K52LV',
        merchantName:'firmware files',
    }
    paymentDataRequest.transactionInfo={
        totalPriceStatus: 'FINAL',
        totalPrice: selectedItem.pirce,
        currencyCode: 'USD',
        countryCode: 'US',
    }

    googlePayClient.loadPaymentData(paymentDataRequest)
      .then(paymentData=>processPaymentData(paymentData))
      .catch(error=> console.error('loadPaymentData error :', error))
}

function processPaymentData(paymentData){
    fetch(ordersEndpointUrl,{
        method: "POST",
        headers:{
            'Content-Type':'application/json'
        },
        body: paymentData,
    })
}

<!-- {% block javascript %}
  <script src="{%static 'js/googlePay.js'%}"></script>

  <script
  async
  src="https://pay.google.com/gp/p/js/pay.js"
  onload="onGooglePayLoaded()">
</script>
{% endblock %} -->