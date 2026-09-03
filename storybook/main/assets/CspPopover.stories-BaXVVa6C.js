import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{A as t,C as n,D as r,Et as i,F as a,G as o,H as s,I as c,O as l,Q as u,S as d,St as f,Z as p,c as m,h,ht as g,q as ee,rt as _,yt as te,z as ne}from"./iframe-BrU2M-Uz.js";import{E as re,T as ie,d as ae,g as oe,i as se,n as v,t as y,y as ce}from"./useForwardExpose-DgXqQxa4.js";import{n as le,t as b}from"./Primitive-2uWfS71D.js";import{n as x,t as S}from"./useId-8aBZX-4r.js";import{a as ue,i as de,n as fe,o as pe,r as C,t as me}from"./FocusScope-CVEgdoD7.js";import{n as he,t as ge}from"./useFocusGuards-BP2F4tbD.js";import{a as _e,c as ve,d as ye,f as be,l as w,n as xe,o as Se,r as Ce,s as we,u as T}from"./PopperContent-D3hL-gIA.js";import{n as Te,t as Ee}from"./Presence-BOXZL8ER.js";import{a as De,n as E,r as Oe,t as ke}from"./Teleport-Dgq6t_-T.js";import{n as Ae,t as D}from"./CspButton-CxiQ4DQ7.js";import{n as je,t as Me}from"./useStoryOpenState-DwtUWx_Z.js";var O,k,A;function j(){return(j=e((()=>{re(),ve(),m(),se(),[O,k]=ie(`PopoverRoot`),A=l({__name:`PopoverRoot`,props:{defaultOpen:{type:Boolean,required:!1,default:!1},open:{type:Boolean,required:!1,default:void 0},modal:{type:Boolean,required:!1,default:!1}},emits:[`update:open`],setup(e,{emit:t}){let n=e,r=t,{modal:i}=te(n),a=ae(n,`open`,r,{defaultValue:n.defaultOpen,passive:n.open===void 0}),c=g(),l=g(!1);return k({contentId:``,triggerId:``,modal:i,open:a,onOpenChange:e=>{a.value=e},onOpenToggle:()=>{a.value=!a.value},triggerElement:c,hasCustomAnchor:l}),(e,t)=>(s(),d(f(we),null,{default:_(()=>[o(e.$slots,`default`,{open:f(a),close:()=>a.value=!1})]),_:3}))}})})))()}var M;function N(){return(N=e((()=>{ge(),y(),ye(),De(),fe(),Ce(),j(),m(),oe(),M=l({__name:`PopoverContentImpl`,props:{trapFocus:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,a=be(ce(n,`trapFocus`,`disableOutsidePointerEvents`)),{forwardRef:l}=v(),u=O();return he(),(e,t)=>(s(),d(f(me),{"as-child":``,loop:``,trapped:e.trapFocus,onMountAutoFocus:t[5]||=e=>i(`openAutoFocus`,e),onUnmountAutoFocus:t[6]||=e=>i(`closeAutoFocus`,e)},{default:_(()=>[r(f(Oe),{"as-child":``,"disable-outside-pointer-events":e.disableOutsidePointerEvents,onPointerDownOutside:t[0]||=e=>i(`pointerDownOutside`,e),onInteractOutside:t[1]||=e=>i(`interactOutside`,e),onEscapeKeyDown:t[2]||=e=>i(`escapeKeyDown`,e),onFocusOutside:t[3]||=e=>i(`focusOutside`,e),onDismiss:t[4]||=e=>f(u).onOpenChange(!1)},{default:_(()=>[r(f(xe),c(f(a),{id:f(u).contentId,ref:f(l),"data-state":f(u).open.value?`open`:`closed`,"aria-labelledby":f(u).triggerId,style:{"--reka-popover-content-transform-origin":`var(--reka-popper-transform-origin)`,"--reka-popover-content-available-width":`var(--reka-popper-available-width)`,"--reka-popover-content-available-height":`var(--reka-popper-available-height)`,"--reka-popover-trigger-width":`var(--reka-popper-anchor-width)`,"--reka-popover-trigger-height":`var(--reka-popper-anchor-height)`},role:`dialog`}),{default:_(()=>[o(e.$slots,`default`)]),_:3},16,[`id`,`data-state`,`aria-labelledby`])]),_:3},8,[`disable-outside-pointer-events`])]),_:3},8,[`trapped`]))}})})))()}var P;function F(){return(F=e((()=>{ue(),y(),w(),C(),j(),N(),m(),P=l({__name:`PopoverContentModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,r=t,i=O(),a=g(!1);pe(!0);let l=T(n,r),{forwardRef:u,currentElement:p}=v();return de(p),(e,t)=>(s(),d(M,c(f(l),{ref:f(u),"trap-focus":f(i).open.value,"disable-outside-pointer-events":``,onCloseAutoFocus:t[0]||=h(e=>{r(`closeAutoFocus`,e),a.value||f(i).triggerElement.value?.focus()},[`prevent`]),onPointerDownOutside:t[1]||=e=>{r(`pointerDownOutside`,e);let t=e.detail.originalEvent,n=t.button===0&&t.ctrlKey===!0,i=t.button===2||n;a.value=i},onFocusOutside:t[2]||=h(()=>{},[`prevent`])}),{default:_(()=>[o(e.$slots,`default`)]),_:3},16,[`trap-focus`]))}})})))()}var I;function L(){return(L=e((()=>{w(),j(),N(),m(),I=l({__name:`PopoverContentNonModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,r=t,i=O(),a=g(!1),l=g(!1),u=T(n,r);return(e,t)=>(s(),d(M,c(f(u),{"trap-focus":!1,"disable-outside-pointer-events":!1,onCloseAutoFocus:t[0]||=e=>{r(`closeAutoFocus`,e),e.defaultPrevented||(a.value||f(i).triggerElement.value?.focus(),e.preventDefault()),a.value=!1,l.value=!1},onInteractOutside:t[1]||=async e=>{r(`interactOutside`,e),e.defaultPrevented||(a.value=!0,e.detail.originalEvent.type===`pointerdown`&&(l.value=!0));let t=e.target;f(i).triggerElement.value?.contains(t)&&e.preventDefault(),e.detail.originalEvent.type===`focusin`&&l.value&&e.preventDefault()}}),{default:_(()=>[o(e.$slots,`default`)]),_:3},16))}})})))()}var R;function z(){return(z=e((()=>{y(),w(),S(),Te(),j(),F(),L(),m(),R=l({__name:`PopoverContent`,props:{forceMount:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,r=t,i=O(),a=T(n,r),{forwardRef:l}=v();return i.contentId||=x(void 0,`reka-popover-content`),(e,t)=>(s(),d(f(Ee),{present:e.forceMount||f(i).open.value},{default:_(()=>[f(i).modal.value?(s(),d(P,c({key:0},f(a),{ref:f(l)}),{default:_(()=>[o(e.$slots,`default`)]),_:3},16)):(s(),d(I,c({key:1},f(a),{ref:f(l)}),{default:_(()=>[o(e.$slots,`default`)]),_:3},16))]),_:3},8,[`present`]))}})})))()}var B;function V(){return(V=e((()=>{E(),m(),B=l({__name:`PopoverPortal`,props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(e){let n=e;return(e,r)=>(s(),d(f(ke),i(t(n)),{default:_(()=>[o(e.$slots,`default`)]),_:3},16))}})})))()}var H;function U(){return(U=e((()=>{y(),S(),le(),Se(),j(),m(),H=l({__name:`PopoverTrigger`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`}},setup(e){let t=e,n=O(),{forwardRef:i,currentElement:a}=v();return n.triggerId||=x(void 0,`reka-popover-trigger`),ne(()=>{n.triggerElement.value=a.value}),(e,a)=>(s(),d(ee(f(n).hasCustomAnchor.value?f(b):f(_e)),{"as-child":``},{default:_(()=>[r(f(b),{id:f(n).triggerId,ref:f(i),type:e.as===`button`?`button`:void 0,"aria-haspopup":`dialog`,"aria-expanded":f(n).open.value,"aria-controls":f(n).contentId,"data-state":f(n).open.value?`open`:`closed`,as:e.as,"as-child":t.asChild,onClick:f(n).onOpenToggle},{default:_(()=>[o(e.$slots,`default`)]),_:3},8,[`id`,`type`,`aria-expanded`,`aria-controls`,`data-state`,`as`,`as-child`,`onClick`])]),_:3}))}})})))()}var W;function G(){return(G=e((()=>{m(),z(),V(),j(),U(),W=l({inheritAttrs:!1,__name:`CspPopover`,props:a({side:{default:`bottom`},align:{default:`start`}},{open:{type:Boolean},openModifiers:{}}),emits:[`update:open`],setup(e){let t=p(e,`open`),i=!!u().trigger;return(a,c)=>(s(),d(f(A),{open:t.value,"onUpdate:open":c[0]||=e=>t.value=e},{default:_(()=>[f(i)?(s(),d(f(H),{key:0,"as-child":``},{default:_(()=>[o(a.$slots,`trigger`)]),_:3})):n(``,!0),r(f(B),null,{default:_(()=>[r(f(R),{class:`csp-popover`,side:e.side,align:e.align,"side-offset":6},{default:_(()=>[o(a.$slots,`default`)]),_:3},8,[`side`,`align`])]),_:3})]),_:3},8,[`open`]))}})})))()}var K;function q(){return(q=e((()=>{G(),K=W})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{Ae(),q(),Me(),J={title:`Éléments/Génériques/CspPopover`,component:K,tags:[`autodocs`],parameters:{controls:{include:[`open`,`side`,`align`]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:`centered`},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Côté d'apparition du popover.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`bottom`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du popover par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:`bottom`,align:`start`},render:e=>({components:{CspPopover:K,CspButton:D},setup(){let{controlledOpen:t,handleUpdateOpen:n,open:r}=je(e);return{args:e,controlledOpen:t,handleUpdateOpen:n,open:r}},template:`
      <CspPopover v-bind="args" :open="controlledOpen" @update:open="handleUpdateOpen">
        <template #trigger>
          <CspButton
            :label="(open ? 'Fermer' : 'Ouvrir') + ' le popover'"
            variant="secondary"
            icon="ri:settings-3-line"
            :is-icon-left="true"
          />
        </template>

        <p class="text-sm">Contenu libre du popover.</p>
      </CspPopover>
    `})},Y={name:`Par défaut`},X={name:`Côtés`,render:e=>({components:{CspPopover:K,CspButton:D},setup(){return{args:e,sides:[{label:`Haut`,value:`top`},{label:`Droite`,value:`right`},{label:`Bas`,value:`bottom`},{label:`Gauche`,value:`left`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},Z={name:`Alignements`,render:e=>({components:{CspPopover:K,CspButton:D},setup(){return{args:e,alignments:[{label:`Début`,value:`start`},{label:`Centre`,value:`center`},{label:`Fin`,value:`end`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Côtés',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const sides = [{
        label: 'Haut',
        value: 'top'
      }, {
        label: 'Droite',
        value: 'right'
      }, {
        label: 'Bas',
        value: 'bottom'
      }, {
        label: 'Gauche',
        value: 'left'
      }] satisfies {
        label: string;
        value: NonNullable<CspPopoverProps['side']>;
      }[];
      return {
        args,
        sides
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Alignements',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const alignments = [{
        label: 'Début',
        value: 'start'
      }, {
        label: 'Centre',
        value: 'center'
      }, {
        label: 'Fin',
        value: 'end'
      }] satisfies {
        label: string;
        value: NonNullable<CspPopoverProps['align']>;
      }[];
      return {
        args,
        alignments
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Sides`,`Alignments`]})))()}$();export{Z as Alignments,Y as Default,X as Sides,Q as __namedExportsOrder,J as default};