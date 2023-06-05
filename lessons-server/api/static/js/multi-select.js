
$(document).ready(function() {
    $(".status-multiple").select2({
      placeholder: "Aktiv/inaktiv",
      allowClear: true
    });
    $(".gender-multiple").select2({
      placeholder: "Køn",
      allowClear: true
    });
});

// $('.status-multiple').on('select2:close', function (e) {
//     console.log("test");
//     var data = e.params.data;
//     console.log(data);
// });

// $('.status-multiple').on("change", function (e) { log("change"); });

/*
  The `select` menus all have an initial option that has no value
  and negates that `select` menu from the final filtering if it is
  selected. Without that initial empty option there would be no means
  by which the filter could be removed.
*/

// let markers=[
//   /*
//     this is an array of the markers. Each marker has attributes that can 
//     be targeted by these filters - such as `gender`, `grade`, `tutor_gym`
    
//     We can check a markers property like: mkr.grade or mkr.gender etc
//     which will be done by the logic in the filtering function - 
//     ie:
//     markers.filter()
    
    
//   */
// ];

// let filters={};
// let CN='filtered';

// const filterMarkers=function(e){
//   // add/remove `filtered` class depending upon option selected
//   if( this.selectedIndex==0 && this.classList.contains( CN ) ){
//     this.classList.remove( CN );
//     if( this.hasAttribute('multiple') ){
//         [...this.options].forEach((o,i)=>{
//           if( filters.hasOwnProperty(`${this.name}[${i}]`) )delete filters[`${this.name}[${i}]`];
//         });
//     }else{
//       delete filters[ this.name ];
//     }
//   }else this.classList.add( CN );

//   // hide all markers
//   if( markers )markers.forEach( mkr=>mkr.setVisible( false ) );



//   /* 
//     process ALL select menus
//     ------------------------
//     Stage 1: prepare filters
//     Stage 2: filter the markers array based upon filters
//     Stage 3: display markers returned after filtering.
//   */

//   // 1 - prepare
//   let col=document.querySelectorAll( `select.${CN}` );
//     col.forEach( n=>{
//       if( n.hasAttribute('multiple') ){
      
//         // delete filters where there is the multiple attribute set
//         [...n.options].forEach((o,i)=>{
//           if( filters.hasOwnProperty(`${n.name}[${i}]`) )delete filters[`${n.name}[${i}]`];
//         });
        
//         // then add only those selected options to the filters...
//         [ ...n.selectedOptions ].forEach((obj,i)=>{
//           filters[ `${n.name}[${i}]`]=obj.value;
//         })

//       }else{
//         filters[ n.name ]=n.value;
//       }
//     });
    
//     // this will show what filters will be applied
//     console.log( filters );

//     // 2 - filter
//     let filtered=markers.filter( function( mkr ){
//       let res=true;
//       Object.keys( filters ).forEach( ( name, i ) => {
//         res = res && filters[ name ]===mkr[ name ];
//       });
//       return res;
//     });

//     // 3 - display
//     filtered.forEach( mkr=>{
//       mkr.setVisible( true );
//     }); 
// };
// const filterSecond=(e)=>console.log('hello world');

// document.querySelectorAll('select.usr-select').forEach( n=>n.addEventListener('change',filterMarkers));

