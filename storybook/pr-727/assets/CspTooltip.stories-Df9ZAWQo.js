import{C as i}from"./CspButton-DdZRQonE.js";import{C as n}from"./CspTooltip-C98Xgrxh.js";import"./vue.esm-bundler-7zVN4DZj.js";import"./Primitive-DzgJnGz8.js";import"./CspIcon-ClPxlQGO.js";import"./iconify-DRloO12f.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";import"./useForwardExpose-Owox9Wch.js";import"./PopperContent-Bhb-IUdV.js";import"./Teleport-BepXBpzl.js";import"./nullish-CHIgUVhi.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./Presence-BwRiO_xX.js";import"./VisuallyHidden-BOK6EsXA.js";const H={title:"Éléments/Génériques/CspTooltip",component:n,tags:["autodocs"],parameters:{controls:{include:["content","side","align","sideOffset","delayDuration","disabled"]},docs:{description:{component:"Infobulle contextuelle affichée au survol ou au focus. Enveloppe un élément déclencheur via le slot par défaut."}}},argTypes:{content:{control:{type:"text"},description:"Texte affiché dans l'infobulle.",table:{type:{summary:"string"}}},side:{control:{type:"radio"},options:["top","right","bottom","left"],description:"Position de l'infobulle par rapport au déclencheur.",table:{type:{summary:"top | right | bottom | left"},defaultValue:{summary:"right"}}},align:{control:{type:"radio"},options:["start","center","end"],description:"Alignement de l'infobulle le long de l'axe perpendiculaire.",table:{type:{summary:"start | center | end"},defaultValue:{summary:"center"}}},sideOffset:{control:{type:"number"},description:"Distance entre l'infobulle et le déclencheur, en pixels.",table:{type:{summary:"number"},defaultValue:{summary:"8"}}},delayDuration:{control:{type:"number"},description:"Délai avant l'affichage, en millisecondes.",table:{type:{summary:"number"},defaultValue:{summary:"200"}}},disabled:{control:{type:"boolean"},description:"Désactive l'infobulle et rend uniquement le contenu du slot.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{content:"Texte de l'infobulle",side:"top",align:"center",sideOffset:8,delayDuration:200,disabled:!1},render:e=>({components:{CspTooltip:n,CspButton:i},setup(){return{args:e}},template:`
      <div class="flex justify-center p-16">
        <CspTooltip v-bind="args">
          <CspButton label="Survolez-moi" />
        </CspTooltip>
      </div>
    `})},$=["top","right","bottom","left"],j=["start","center","end"],t={},s={render:e=>({components:{CspTooltip:n,CspButton:i},setup(){return{sides:$,args:e}},template:`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="side in sides"
          :key="side"
          class="flex flex-col items-center gap-2"
        >
          <CspTooltip
            v-bind="args"
            :side="side"
            :content="\`Position \${side}\`"
          >
            <CspButton
              :label="side"
              variant="secondary"
            />
          </CspTooltip>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},a={render:e=>({components:{CspTooltip:n,CspButton:i},setup(){return{aligns:j,args:e}},template:`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="align in aligns"
          :key="align"
          class="flex flex-col items-center gap-2"
        >
          <CspTooltip
            v-bind="args"
            side="bottom"
            :align="align"
            :content="\`Alignement \${align}\`"
          >
            <CspButton
              :label="align"
              variant="tertiary"
            />
          </CspTooltip>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},r={args:{content:"Infobulle avec un contenu plus long pour vérifier le retour à la ligne et la largeur maximale."}},l={args:{content:"Ce texte ne s'affichera pas",disabled:!0}},o={render:e=>({components:{CspTooltip:n,CspButton:i},setup(){return{delays:[0,200,800],args:e}},template:`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="delay in delays"
          :key="delay"
          class="flex flex-col items-center gap-2"
        >
          <p class="text-sm">{{ delay }} ms</p>
          <CspTooltip
            v-bind="args"
            :delay-duration="delay"
            :content="\`Délai de \${delay} ms\`"
          >
            <CspButton
              :label="\`\${delay} ms\`"
              variant="tertiary"
            />
          </CspTooltip>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}};var p,d,c;t.parameters={...t.parameters,docs:{...(p=t.parameters)==null?void 0:p.docs,source:{originalSource:"{}",...(c=(d=t.parameters)==null?void 0:d.docs)==null?void 0:c.source}}};var u,m,f;s.parameters={...s.parameters,docs:{...(u=s.parameters)==null?void 0:u.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspTooltip,
      CspButton
    },
    setup() {
      return {
        sides: SIDES,
        args
      };
    },
    template: \`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="side in sides"
          :key="side"
          class="flex flex-col items-center gap-2"
        >
          <CspTooltip
            v-bind="args"
            :side="side"
            :content="\\\`Position \\\${side}\\\`"
          >
            <CspButton
              :label="side"
              variant="secondary"
            />
          </CspTooltip>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(f=(m=s.parameters)==null?void 0:m.docs)==null?void 0:f.source}}};var g,y,b;a.parameters={...a.parameters,docs:{...(g=a.parameters)==null?void 0:g.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspTooltip,
      CspButton
    },
    setup() {
      return {
        aligns: ALIGNS,
        args
      };
    },
    template: \`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="align in aligns"
          :key="align"
          class="flex flex-col items-center gap-2"
        >
          <CspTooltip
            v-bind="args"
            side="bottom"
            :align="align"
            :content="\\\`Alignement \\\${align}\\\`"
          >
            <CspButton
              :label="align"
              variant="tertiary"
            />
          </CspTooltip>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(b=(y=a.parameters)==null?void 0:y.docs)==null?void 0:b.source}}};var v,x,C;r.parameters={...r.parameters,docs:{...(v=r.parameters)==null?void 0:v.docs,source:{originalSource:`{
  args: {
    content: 'Infobulle avec un contenu plus long pour vérifier le retour à la ligne et la largeur maximale.'
  }
}`,...(C=(x=r.parameters)==null?void 0:x.docs)==null?void 0:C.source}}};var T,D,S;l.parameters={...l.parameters,docs:{...(T=l.parameters)==null?void 0:T.docs,source:{originalSource:`{
  args: {
    content: 'Ce texte ne s\\'affichera pas',
    disabled: true
  }
}`,...(S=(D=l.parameters)==null?void 0:D.docs)==null?void 0:S.source}}};var h,B,k;o.parameters={...o.parameters,docs:{...(h=o.parameters)==null?void 0:h.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspTooltip,
      CspButton
    },
    setup() {
      return {
        delays: [0, 200, 800] as const,
        args
      };
    },
    template: \`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="delay in delays"
          :key="delay"
          class="flex flex-col items-center gap-2"
        >
          <p class="text-sm">{{ delay }} ms</p>
          <CspTooltip
            v-bind="args"
            :delay-duration="delay"
            :content="\\\`Délai de \\\${delay} ms\\\`"
          >
            <CspButton
              :label="\\\`\\\${delay} ms\\\`"
              variant="tertiary"
            />
          </CspTooltip>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(k=(B=o.parameters)==null?void 0:B.docs)==null?void 0:k.source}}};const J=["Default","Positions","Alignments","LongContent","Disabled","Delays"];export{a as Alignments,t as Default,o as Delays,l as Disabled,r as LongContent,s as Positions,J as __namedExportsOrder,H as default};
