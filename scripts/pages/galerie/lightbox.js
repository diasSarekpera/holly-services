(function(){
  var links=[].slice.call(document.querySelectorAll('[data-lightbox]'));
  if(!links.length)return;
  var box=document.createElement('div');box.className='lb';box.hidden=true;
  box.innerHTML='<button class="lb__x" type="button" aria-label="Fermer">×</button><button class="lb__p" type="button" aria-label="Photo précédente">‹</button><img class="lb__img" alt=""><button class="lb__n" type="button" aria-label="Photo suivante">›</button>';
  document.body.appendChild(box);
  var img=box.querySelector('.lb__img'),i=0,last=null;
  function show(n){i=(n+links.length)%links.length;img.src=links[i].getAttribute('href');img.alt=links[i].querySelector('img').alt;}
  function open(n,t){last=t;show(n);box.hidden=false;document.body.style.overflow='hidden';box.querySelector('.lb__x').focus();}
  function close(){box.hidden=true;document.body.style.overflow='';if(last)last.focus();}
  links.forEach(function(a,n){a.addEventListener('click',function(e){e.preventDefault();open(n,a);});});
  box.querySelector('.lb__x').onclick=close;
  box.querySelector('.lb__p').onclick=function(){show(i-1)};
  box.querySelector('.lb__n').onclick=function(){show(i+1)};
  box.addEventListener('click',function(e){if(e.target===box)close();});
  document.addEventListener('keydown',function(e){if(box.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});
})();
