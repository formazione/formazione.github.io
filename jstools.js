/*   --- RACCOLTA DI FUNZIONI JAVASCRIPT  ---
                    LISTA
                    -----
                    
noscrollbars      non mostra scrollbars    30.1.2019
shuffle           mischia array            30.1.2019
*/


function noscrollbars(){
  // disables scrollbars
  document.documentElement.style.overflow = 'hidden';  // firefox, chrome
}

function shuffle(list){
  // restituisce un array mischiato
    list.sort(function() {
      return .5 - Math.random();
    });
return list;};