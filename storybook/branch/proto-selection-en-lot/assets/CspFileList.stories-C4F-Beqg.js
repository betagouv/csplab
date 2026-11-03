import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{t,yt as n}from"./vue.esm-bundler-BdiU-5Kf.js";import{n as r,t as i}from"./CspFileList-DES3o18i.js";var a,o,s;function c(){return(c=e((()=>{t(),r(),a={title:`Éléments/Génériques/CspFileList`,component:i,tags:[`autodocs`],parameters:{docs:{description:{component:`Liste de fichiers prêts à envoyer : icône, nom, poids et bouton « Retirer » par ligne, avec le message d'erreur d'un fichier refusé. La liste est une région \`aria-live="polite"\` : les lecteurs d'écran annoncent les fichiers ajoutés et leurs erreurs. Après un retrait, le focus passe au bouton de la ligne suivante, ou de la précédente ; quand la liste se vide, la vue replace le focus, par exemple sur le bouton d'ajout.`}},controls:{disable:!0}},args:{label:`Fichiers`,items:[]}},o={name:`Par défaut`,render:()=>({components:{CspFileList:i},setup(){let e=n([{key:`a`,name:`document-a.pdf`,size:82e4},{key:`b`,name:`document-b.pdf`,size:31e4},{key:`c`,name:`image-trop-lourde.jpg`,size:124e5,error:`Le fichier dépasse 10 Mo.`}]);return{items:e,remove:t=>{e.value=e.value.filter(e=>e.key!==t)}}},template:`<CspFileList label="Fichiers" :items="items" @remove="remove" />`})},s=[`Default`],o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  render: () => ({
    components: {
      CspFileList
    },
    setup() {
      const items = ref([{
        key: 'a',
        name: 'document-a.pdf',
        size: 820_000
      }, {
        key: 'b',
        name: 'document-b.pdf',
        size: 310_000
      }, {
        key: 'c',
        name: 'image-trop-lourde.jpg',
        size: 12_400_000,
        error: 'Le fichier dépasse 10 Mo.'
      }]);
      const remove = (key: string) => {
        items.value = items.value.filter(item => item.key !== key);
      };
      return {
        items,
        remove
      };
    },
    template: \`<CspFileList label="Fichiers" :items="items" @remove="remove" />\`
  })
}`,...o.parameters?.docs?.source}}}})))()}c();export{o as Default,s as __namedExportsOrder,a as default};