import{a as V,k as q}from"./useForwardExpose-Owox9Wch.js";import{u as N}from"./useId-Blg3GNwK.js";import{P as A}from"./Primitive-DzgJnGz8.js";import{l as c,K as M,f as w,ab as D,Q as I,y as j,a1 as r,B as $,p as E}from"./vue.esm-bundler-7zVN4DZj.js";import{D as s,_ as t,a as f}from"./CspDropdownMenu-BJiT561z.js";import{C as a}from"./CspButton-DdZRQonE.js";import{_ as g}from"./CspIcon-ClPxlQGO.js";import"./Teleport-BepXBpzl.js";import"./nullish-CHIgUVhi.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./utils-D0uXTaE0.js";import"./ConfigProvider-BVLqxNYe.js";import"./RovingFocusGroup-C-W6CSoP.js";import"./usePrimitiveElement-BQYvfrMI.js";import"./PopperContent-Bhb-IUdV.js";import"./Presence-BoZiCw1w.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";import"./iconify-DRloO12f.js";const[F,K]=V("MenuGroup");var Q=c({__name:"MenuGroup",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){const o=e,n=N(void 0,"reka-menu-group");return K({id:n}),(p,W)=>(M(),w(r(A),j({role:"group"},o,{"aria-labelledby":r(n)}),{default:D(()=>[I(p.$slots,"default")]),_:3},16,["aria-labelledby"]))}}),R=Q,T=c({__name:"MenuLabel",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:"div"}},setup(e){const o=e,n=F({id:""});return(p,W)=>(M(),w(r(A),j(o,{id:r(n).id||void 0}),{default:D(()=>[I(p.$slots,"default")]),_:3},16,["id"]))}}),U=T,H=c({__name:"DropdownMenuGroup",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){const o=e;return q(),(n,p)=>(M(),w(r(R),$(E(o)),{default:D(()=>[I(n.$slots,"default")]),_:3},16))}}),J=H,X=c({__name:"DropdownMenuLabel",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){const o=e;return q(),(n,p)=>(M(),w(r(U),$(E(o)),{default:D(()=>[I(n.$slots,"default")]),_:3},16))}}),Y=X;const ge={title:"Éléments/Génériques/CspDropdownMenu",component:t,tags:["autodocs"],parameters:{controls:{include:["align","side","sideOffset"]},docs:{description:{component:"Menu déroulant accessible basé sur les primitives `reka-ui`. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour les items du menu."}}},argTypes:{align:{control:{type:"radio"},options:["start","center","end"],description:"Alignement du menu par rapport au déclencheur.",table:{type:{summary:"start | center | end"},defaultValue:{summary:"start"}}},side:{control:{type:"radio"},options:["top","right","bottom","left"],description:"Position du menu par rapport au déclencheur.",table:{type:{summary:"top | right | bottom | left"},defaultValue:{summary:"top"}}},sideOffset:{control:{type:"number"},description:"Distance entre le menu et le déclencheur, en pixels.",table:{type:{summary:"number"},defaultValue:{summary:"8"}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{align:"start",side:"bottom",sideOffset:8},render:e=>({components:{CspDropdownMenu:t,DropdownMenuItem:s,DropdownMenuSeparator:f,CspButton:a,CspIcon:g},setup(){return{args:e}},template:`
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Ouvrir le menu" variant="secondary" />
          </template>

          <DropdownMenuItem>
            <CspIcon name="ri:user-line" :size="16" />
            Mon profil
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CspIcon name="ri:settings-3-line" :size="16" />
            Paramètres
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <CspIcon name="ri:logout-box-r-line" :size="16" />
            Se déconnecter
          </DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `})},Z=["top","right","bottom","left"],ee=["start","center","end"],u={},d={render:e=>({components:{CspDropdownMenu:t,DropdownMenuItem:s,CspButton:a},setup(){return{sides:Z,args:e}},template:`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <CspDropdownMenu
          v-for="side in sides"
          :key="side"
          v-bind="args"
          :side="side"
        >
          <template #trigger>
            <CspButton :label="side" variant="secondary" />
          </template>

          <DropdownMenuItem>Option 1</DropdownMenuItem>
          <DropdownMenuItem>Option 2</DropdownMenuItem>
          <DropdownMenuItem>Option 3</DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `}),parameters:{controls:{disable:!0}}},i={render:e=>({components:{CspDropdownMenu:t,DropdownMenuItem:s,CspButton:a},setup(){return{aligns:ee,args:e}},template:`
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <CspDropdownMenu
          v-for="align in aligns"
          :key="align"
          v-bind="args"
          side="bottom"
          :align="align"
        >
          <template #trigger>
            <CspButton :label="align" variant="tertiary" />
          </template>

          <DropdownMenuItem>Option 1</DropdownMenuItem>
          <DropdownMenuItem>Option 2</DropdownMenuItem>
          <DropdownMenuItem>Option 3</DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `}),parameters:{controls:{disable:!0}}},l={render:e=>({components:{CspDropdownMenu:t,DropdownMenuGroup:J,DropdownMenuItem:s,DropdownMenuLabel:Y,DropdownMenuSeparator:f,CspButton:a,CspIcon:g},setup(){return{args:e}},template:`
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Menu avec groupes" variant="secondary" />
          </template>

          <DropdownMenuLabel>Mon compte</DropdownMenuLabel>
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <CspIcon name="ri:user-line" :size="16" />
              Profil
            </DropdownMenuItem>
            <DropdownMenuItem>
              <CspIcon name="ri:settings-3-line" :size="16" />
              Paramètres
            </DropdownMenuItem>
          </DropdownMenuGroup>

          <DropdownMenuSeparator />

          <DropdownMenuLabel>Équipe</DropdownMenuLabel>
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <CspIcon name="ri:group-line" :size="16" />
              Membres
            </DropdownMenuItem>
            <DropdownMenuItem>
              <CspIcon name="ri:add-line" :size="16" />
              Inviter
            </DropdownMenuItem>
          </DropdownMenuGroup>

          <DropdownMenuSeparator />

          <DropdownMenuItem>
            <CspIcon name="ri:logout-box-r-line" :size="16" />
            Se déconnecter
          </DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `})},m={render:e=>({components:{CspDropdownMenu:t,DropdownMenuItem:s,DropdownMenuSeparator:f,CspButton:a,CspIcon:g},setup(){return{args:e}},template:`
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Actions" variant="primary" />
          </template>

          <DropdownMenuItem>
            <CspIcon name="ri:edit-line" :size="16" />
            Modifier
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CspIcon name="ri:eye-line" :size="16" />
            Aperçu
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CspIcon name="ri:external-link-line" :size="16" />
            Ouvrir dans un nouvel onglet
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <CspIcon name="ri:delete-bin-line" :size="16" />
            Supprimer
          </DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `})};var b,C,v;u.parameters={...u.parameters,docs:{...(b=u.parameters)==null?void 0:b.docs,source:{originalSource:"{}",...(v=(C=u.parameters)==null?void 0:C.docs)==null?void 0:v.source}}};var _,y,S;d.parameters={...d.parameters,docs:{...(_=d.parameters)==null?void 0:_.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDropdownMenu,
      DropdownMenuItem,
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
        <CspDropdownMenu
          v-for="side in sides"
          :key="side"
          v-bind="args"
          :side="side"
        >
          <template #trigger>
            <CspButton :label="side" variant="secondary" />
          </template>

          <DropdownMenuItem>Option 1</DropdownMenuItem>
          <DropdownMenuItem>Option 2</DropdownMenuItem>
          <DropdownMenuItem>Option 3</DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(S=(y=d.parameters)==null?void 0:y.docs)==null?void 0:S.source}}};var x,G,z;i.parameters={...i.parameters,docs:{...(x=i.parameters)==null?void 0:x.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDropdownMenu,
      DropdownMenuItem,
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
        <CspDropdownMenu
          v-for="align in aligns"
          :key="align"
          v-bind="args"
          side="bottom"
          :align="align"
        >
          <template #trigger>
            <CspButton :label="align" variant="tertiary" />
          </template>

          <DropdownMenuItem>Option 1</DropdownMenuItem>
          <DropdownMenuItem>Option 2</DropdownMenuItem>
          <DropdownMenuItem>Option 3</DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(z=(G=i.parameters)==null?void 0:G.docs)==null?void 0:z.source}}};var B,h,L;l.parameters={...l.parameters,docs:{...(B=l.parameters)==null?void 0:B.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDropdownMenu,
      DropdownMenuGroup,
      DropdownMenuItem,
      DropdownMenuLabel,
      DropdownMenuSeparator,
      CspButton,
      CspIcon
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Menu avec groupes" variant="secondary" />
          </template>

          <DropdownMenuLabel>Mon compte</DropdownMenuLabel>
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <CspIcon name="ri:user-line" :size="16" />
              Profil
            </DropdownMenuItem>
            <DropdownMenuItem>
              <CspIcon name="ri:settings-3-line" :size="16" />
              Paramètres
            </DropdownMenuItem>
          </DropdownMenuGroup>

          <DropdownMenuSeparator />

          <DropdownMenuLabel>Équipe</DropdownMenuLabel>
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <CspIcon name="ri:group-line" :size="16" />
              Membres
            </DropdownMenuItem>
            <DropdownMenuItem>
              <CspIcon name="ri:add-line" :size="16" />
              Inviter
            </DropdownMenuItem>
          </DropdownMenuGroup>

          <DropdownMenuSeparator />

          <DropdownMenuItem>
            <CspIcon name="ri:logout-box-r-line" :size="16" />
            Se déconnecter
          </DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    \`
  })
}`,...(L=(h=l.parameters)==null?void 0:h.docs)==null?void 0:L.source}}};var O,k,P;m.parameters={...m.parameters,docs:{...(O=m.parameters)==null?void 0:O.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDropdownMenu,
      DropdownMenuItem,
      DropdownMenuSeparator,
      CspButton,
      CspIcon
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Actions" variant="primary" />
          </template>

          <DropdownMenuItem>
            <CspIcon name="ri:edit-line" :size="16" />
            Modifier
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CspIcon name="ri:eye-line" :size="16" />
            Aperçu
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CspIcon name="ri:external-link-line" :size="16" />
            Ouvrir dans un nouvel onglet
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <CspIcon name="ri:delete-bin-line" :size="16" />
            Supprimer
          </DropdownMenuItem>
        </CspDropdownMenu>
      </div>
    \`
  })
}`,...(P=(k=m.parameters)==null?void 0:k.docs)==null?void 0:P.source}}};const be=["Default","Positions","Alignments","WithLabelsAndGroups","WithIcons"];export{i as Alignments,u as Default,d as Positions,m as WithIcons,l as WithLabelsAndGroups,be as __namedExportsOrder,ge as default};
