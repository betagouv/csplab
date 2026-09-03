import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspPageContainer-C1axsf19.js";var r,i,a;function o(){return(o=e((()=>{t(),r={title:`Compositions/Génériques/CspPageContainer`,component:n,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`width`,`fill`]},docs:{description:{component:"Conteneur de page, sert de référence aux container queries (`@container page`). Voir DDR-005."}}},argTypes:{width:{control:{type:`select`},options:[`reading`,`wide`,`large`,`full`],description:`Largeur du contenu.`,table:{type:{summary:`'reading' | 'wide' | 'large' | 'full'`},defaultValue:{summary:`'wide'`}}}}},i={name:`Largeurs`,args:{width:`reading`},render:e=>({components:{CspPageContainer:n},setup(){return{args:e,widths:[`reading`,`wide`,`large`,`full`]}},template:`
      <div class="flex flex-col">
        <CspPageContainer v-for="width in widths" :key="width" v-bind="args" :width="width">
          <div class="border border-dashed border-(--border-default-grey) p-4">
            Contenu du conteneur (largeur : {{ width }})
          </div>
        </CspPageContainer>
      </div>
    `})},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Largeurs',
  args: {
    width: 'reading'
  },
  render: (args: CspPageContainerProps) => ({
    components: {
      CspPageContainer
    },
    setup() {
      const widths = ['reading', 'wide', 'large', 'full'] as const;
      return {
        args,
        widths
      };
    },
    template: \`
      <div class="flex flex-col">
        <CspPageContainer v-for="width in widths" :key="width" v-bind="args" :width="width">
          <div class="border border-dashed border-(--border-default-grey) p-4">
            Contenu du conteneur (largeur : {{ width }})
          </div>
        </CspPageContainer>
      </div>
    \`
  })
}`,...i.parameters?.docs?.source}}},a=[`Widths`]})))()}o();export{i as Widths,a as __namedExportsOrder,r as default};