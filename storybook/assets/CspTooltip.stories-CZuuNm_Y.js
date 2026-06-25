import{i as e}from"./preload-helper-DXs2ar-j.js";import{n as t,t as n}from"./CspButton-CGZTdMzE.js";import{n as r,t as i}from"./CspTooltip-WO87vxKF.js";var a,o,s,c,l,u,d,f,p,m;e((()=>{t(),r(),a={title:`Éléments/Génériques/CspTooltip`,component:i,tags:[`autodocs`],parameters:{controls:{include:[`content`,`side`,`align`,`sideOffset`,`delayDuration`,`disabled`]},docs:{description:{component:`Infobulle contextuelle affichée au survol ou au focus. Enveloppe un élément déclencheur via le slot par défaut.`}}},argTypes:{content:{control:{type:`text`},description:`Texte affiché dans l'infobulle.`,table:{type:{summary:`string`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Position de l'infobulle par rapport au déclencheur.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`right`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement de l'infobulle le long de l'axe perpendiculaire.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`center`}}},sideOffset:{control:{type:`number`},description:`Distance entre l'infobulle et le déclencheur, en pixels.`,table:{type:{summary:`number`},defaultValue:{summary:`8`}}},delayDuration:{control:{type:`number`},description:`Délai avant l'affichage, en millisecondes.`,table:{type:{summary:`number`},defaultValue:{summary:`200`}}},disabled:{control:{type:`boolean`},description:`Désactive l'infobulle et rend uniquement le contenu du slot.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{content:`Texte de l'infobulle`,side:`top`,align:`center`,sideOffset:8,delayDuration:200,disabled:!1},render:e=>({components:{CspTooltip:i,CspButton:n},setup(){return{args:e}},template:`
      <div class="flex justify-center p-16">
        <CspTooltip v-bind="args">
          <CspButton label="Survolez-moi" />
        </CspTooltip>
      </div>
    `})},o=[`top`,`right`,`bottom`,`left`],s=[`start`,`center`,`end`],c={},l={render:e=>({components:{CspTooltip:i,CspButton:n},setup(){return{sides:o,args:e}},template:`
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
    `}),parameters:{controls:{disable:!0}}},u={render:e=>({components:{CspTooltip:i,CspButton:n},setup(){return{aligns:s,args:e}},template:`
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
    `}),parameters:{controls:{disable:!0}}},d={args:{content:`Infobulle avec un contenu plus long pour vérifier le retour à la ligne et la largeur maximale.`}},f={args:{content:`Ce texte ne s'affichera pas`,disabled:!0}},p={render:e=>({components:{CspTooltip:i,CspButton:n},setup(){return{delays:[0,200,800],args:e}},template:`
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
    `}),parameters:{controls:{disable:!0}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
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
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  args: {
    content: 'Infobulle avec un contenu plus long pour vérifier le retour à la ligne et la largeur maximale.'
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    content: 'Ce texte ne s\\'affichera pas',
    disabled: true
  }
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
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
}`,...p.parameters?.docs?.source}}},m=[`Default`,`Positions`,`Alignments`,`LongContent`,`Disabled`,`Delays`]}))();export{u as Alignments,c as Default,p as Delays,f as Disabled,d as LongContent,l as Positions,m as __namedExportsOrder,a as default};