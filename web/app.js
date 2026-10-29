(async function(){
 const editor=document.getElementById('editor'), status=document.getElementById('status');
 try{
  const res=await fetch('./onnoy.js',{method:'HEAD',cache:'no-store'});
  if(!res.ok || !window.keyman) throw new Error('KeymanWeb or compiled keyboard unavailable');
  await keyman.init({attachType:'manual',ui:'float',setActiveOnRegister:false});
  keyman.attachToControl(editor);
  await keyman.addKeyboards({id:'onnoy',name:'Onnoy (অন্বয়)',filename:'./onnoy.js',version:'1.0',languages:[{id:'bn',name:'Bangla'}]});
  await keyman.setActiveKeyboard('onnoy','bn');
  editor.disabled=false;editor.focus();status.textContent='Keyboard ready';
 }catch(e){status.textContent='Keyboard unavailable';console.error(e);}
 const codes=document.getElementById('codepoints');
 const update=()=>{if(!codes.hidden)codes.textContent=Array.from(editor.value).map(c=>c+' U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')).join(' · ');};
 document.getElementById('clear').onclick=()=>{editor.value='';update();editor.focus()};
 document.getElementById('copy').onclick=()=>navigator.clipboard.writeText(editor.value);
 document.getElementById('unicode').onclick=()=>{codes.hidden=!codes.hidden;update()};
 editor.addEventListener('input',update);
})();
