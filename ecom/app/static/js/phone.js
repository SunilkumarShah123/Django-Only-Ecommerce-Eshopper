const input = document.querySelector("#phone");
const validated_number=window.intlTelInput(input, {
  initialCountry: "np",
  strictMode: true,
  loadUtils: () => import("https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/25.2.1/build/js/utils.js") // for formatting/placeholders etc
});

document.getElementById('contactForm').addEventListener('submit',function(e){
   if(validated_number.isValidNumber()){
    input.validate=validated_number.getNumber()
   }else{
    e.preventDefault()
   }
})