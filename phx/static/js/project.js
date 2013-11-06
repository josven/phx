var previewTextarea = function(h) {
  alert('lol');
  console.log(h);
}

var testvar;

$(function ()
{
  textileSettings = {
      nameSpace:           "textile", // Useful to prevent multi-instances CSS conflict
      previewParserPath:   "~/sets/textile/preview.php",
      onShiftEnter:        {keepDefault:false, replaceWith:'\n\n'},
      markupSet: [
          {name:'Rubrik 1', key:'1', openWith:'h1(!(([![Class]!]))!). ', placeHolder:'Din rubrik här...' },
          {name:'Rubrik 2', key:'2', openWith:'h2(!(([![Class]!]))!). ', placeHolder:'Din rubrik här...' },
          {name:'Rubrik 3', key:'3', openWith:'h3(!(([![Class]!]))!). ', placeHolder:'Din rubrik här...' },
          {name:'Rubrik 4', key:'4', openWith:'h4(!(([![Class]!]))!). ', placeHolder:'Din rubrik här...' },
          {name:'Rubrik 5', key:'5', openWith:'h5(!(([![Class]!]))!). ', placeHolder:'Din rubrik här...' },
          {name:'Rubrik 6', key:'6', openWith:'h6(!(([![Class]!]))!). ', placeHolder:'Din rubrik här...' },
          {name:'Paragraf', key:'P', openWith:'p(!(([![Class]!]))!). '}, 
          {separator:'---------------' },
          {name:'Fetstil', key:'B', closeWith:'*', openWith:'*'}, 
          {name:'Kursiv', key:'I', closeWith:'_', openWith:'_'}, 
          {name:'Genomstruken', key:'S', closeWith:'-', openWith:'-'}, 
          {separator:'---------------' },
          {name:'Lista', openWith:'(!(* |!|*)!)'}, 
          {name:'Numrerad lista', openWith:'(!(# |!|#)!)'}, 
          {separator:'---------------' },
          {name:'Bild', replaceWith:'![![Source:!:http://]!]([![Alternative text]!])!'}, 
          {name:'Länk', openWith:'"', closeWith:'([![Title]!])":[![Link:!:http://]!]', placeHolder:'Your text to link here...' },
          {separator:'---------------' },
          {name:'Citat', openWith:'bq(!(([![Class]!]))!). '}, 
          {name:'Kod', openWith:'@', closeWith:'@'}, 
          {separator:'---------------' },       
          {name:'Förhandsgranskning', beforeInsert:function(h) {
            var preview_data = $(h.textarea).val();

            $.post("/utils/preview/", { preview: preview_data })
              .done(function(data) {
                $(data).modal();
            });

          }, className:'preview'},
          {name:'Storskärm', beforeInsert:function(h) {
            element = $(h.textarea).parent('.markItUpContainer');
            element.toggleClass('maximized');
          },
          className:'maximize'}
      ]
  }

  $(".tag").popover({placement:'top'});  
  $('[data-toggle=tooltip]').tooltip();
  $(".media-content a").oembed();
  $("#markItUp").markItUp(textileSettings);

}); 