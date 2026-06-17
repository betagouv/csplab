import{i as e}from"./preload-helper-DXs2ar-j.js";import{B as t,J as n,K as r,W as i,t as a}from"./dist-DnoCvs-A.js";import{n as o,t as s}from"./CspIcon-Dy6iOpSj.js";import{n as c,t as l}from"./CspButton-Cp8lmiPH.js";import{n as u,t as d}from"./CspDropdownMenu-laHk0yhC.js";var f,p,m,h,g,_,v,y,b;e((()=>{a(),c(),u(),o(),f={title:`Éléments/Génériques/CspDropdownMenu`,component:d,tags:[`autodocs`],parameters:{controls:{include:[`align`,`side`,`sideOffset`]},docs:{description:{component:"Menu déroulant accessible basé sur les primitives `reka-ui`. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour les items du menu."}}},argTypes:{align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du menu par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Position du menu par rapport au déclencheur.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`top`}}},sideOffset:{control:{type:`number`},description:`Distance entre le menu et le déclencheur, en pixels.`,table:{type:{summary:`number`},defaultValue:{summary:`8`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{align:`start`,side:`bottom`,sideOffset:8},render:e=>({components:{CspDropdownMenu:d,DropdownMenuItem:r,DropdownMenuSeparator:t,CspButton:l,CspIcon:s},setup(){return{args:e}},template:`
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
    `})},p=[`top`,`right`,`bottom`,`left`],m=[`start`,`center`,`end`],h={},g={render:e=>({components:{CspDropdownMenu:d,DropdownMenuItem:r,CspButton:l},setup(){return{sides:p,args:e}},template:`
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
    `}),parameters:{controls:{disable:!0}}},_={render:e=>({components:{CspDropdownMenu:d,DropdownMenuItem:r,CspButton:l},setup(){return{aligns:m,args:e}},template:`
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
    `}),parameters:{controls:{disable:!0}}},v={render:e=>({components:{CspDropdownMenu:d,DropdownMenuGroup:n,DropdownMenuItem:r,DropdownMenuLabel:i,DropdownMenuSeparator:t,CspButton:l,CspIcon:s},setup(){return{args:e}},template:`
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
    `})},y={render:e=>({components:{CspDropdownMenu:d,DropdownMenuItem:r,DropdownMenuSeparator:t,CspButton:l,CspIcon:s},setup(){return{args:e}},template:`
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
    `})},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{}`,...h.parameters?.docs?.source}}},g.parameters={...g.parameters,docs:{...g.parameters?.docs,source:{originalSource:`{
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
}`,...g.parameters?.docs?.source}}},_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
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
}`,..._.parameters?.docs?.source}}},v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
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
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
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
}`,...y.parameters?.docs?.source}}},b=[`Default`,`Positions`,`Alignments`,`WithLabelsAndGroups`,`WithIcons`]}))();export{_ as Alignments,h as Default,g as Positions,y as WithIcons,v as WithLabelsAndGroups,b as __namedExportsOrder,f as default};