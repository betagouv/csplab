import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{A as t,E as n,G as r,H as i,J as a,N as o,R as s,St as c,T as l,Tt as u,X as d,c as f,et as ee,j as p,kt as te,ot as m,tt as h,v as g,vt as _,z as v}from"./iframe-BQyWb_Zl.js";import{E as ne,T as re,d as ie,g as ae,i as oe,n as y,t as b,y as se}from"./useForwardExpose-YeztB0Lg.js";import{n as ce,t as x}from"./Primitive-lMdUBGMr.js";import{n as S,t as C}from"./useId-klMpLFNL.js";import{a as le,i as ue,n as de,o as fe,r as pe,t as me}from"./FocusScope-5rhPb1JB.js";import{n as he,t as ge}from"./useFocusGuards-CTgBthh_.js";import{a as _e,c as ve,d as ye,f as be,l as w,n as xe,o as Se,r as Ce,s as we,u as T}from"./PopperContent-Bo9hUXNJ.js";import{n as Te,t as Ee}from"./Presence-DgL2hsE7.js";import{a as De,n as E,r as Oe,t as ke}from"./Teleport-s_8zj-7W.js";import{n as Ae,t as D}from"./CspButton-CihLHijh.js";import{n as je,t as Me}from"./useStoryOpenState-Db5E3Qho.js";var O,k,A;function j(){return(j=e((()=>{ne(),ve(),f(),oe(),[O,k]=re(`PopoverRoot`),A=p({__name:`PopoverRoot`,props:{defaultOpen:{type:Boolean,required:!1,default:!1},open:{type:Boolean,required:!1,default:void 0},modal:{type:Boolean,required:!1,default:!1}},emits:[`update:open`],setup(e,{emit:t}){let n=e,i=t,{modal:o}=c(n),s=ie(n,`open`,i,{defaultValue:n.defaultOpen,passive:n.open===void 0}),d=_(),f=_(!1);return k({contentId:``,triggerId:``,modal:o,open:s,onOpenChange:e=>{s.value=e},onOpenToggle:()=>{s.value=!s.value},triggerElement:d,hasCustomAnchor:f}),(e,t)=>(r(),l(u(we),null,{default:m(()=>[a(e.$slots,`default`,{open:u(s),close:()=>s.value=!1})]),_:3}))}})})))()}var M;function N(){return(N=e((()=>{ge(),b(),ye(),De(),de(),Ce(),j(),f(),ae(),M=p({__name:`PopoverContentImpl`,props:{trapFocus:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:n}){let i=e,o=n,s=be(se(i,`trapFocus`,`disableOutsidePointerEvents`)),{forwardRef:c}=y(),d=O();return he(),(e,n)=>(r(),l(u(me),{"as-child":``,loop:``,trapped:e.trapFocus,onMountAutoFocus:n[5]||=e=>o(`openAutoFocus`,e),onUnmountAutoFocus:n[6]||=e=>o(`closeAutoFocus`,e)},{default:m(()=>[t(u(Oe),{"as-child":``,"disable-outside-pointer-events":e.disableOutsidePointerEvents,onPointerDownOutside:n[0]||=e=>o(`pointerDownOutside`,e),onInteractOutside:n[1]||=e=>o(`interactOutside`,e),onEscapeKeyDown:n[2]||=e=>o(`escapeKeyDown`,e),onFocusOutside:n[3]||=e=>o(`focusOutside`,e),onDismiss:n[4]||=e=>u(d).onOpenChange(!1)},{default:m(()=>[t(u(xe),v(u(s),{id:u(d).contentId,ref:u(c),"data-state":u(d).open.value?`open`:`closed`,"aria-labelledby":u(d).triggerId,style:{"--reka-popover-content-transform-origin":`var(--reka-popper-transform-origin)`,"--reka-popover-content-available-width":`var(--reka-popper-available-width)`,"--reka-popover-content-available-height":`var(--reka-popper-available-height)`,"--reka-popover-trigger-width":`var(--reka-popper-anchor-width)`,"--reka-popover-trigger-height":`var(--reka-popper-anchor-height)`},role:`dialog`}),{default:m(()=>[a(e.$slots,`default`)]),_:3},16,[`id`,`data-state`,`aria-labelledby`])]),_:3},8,[`disable-outside-pointer-events`])]),_:3},8,[`trapped`]))}})})))()}var P;function F(){return(F=e((()=>{le(),b(),w(),pe(),j(),N(),f(),P=p({__name:`PopoverContentModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,o=O(),s=_(!1);fe(!0);let c=T(n,i),{forwardRef:d,currentElement:f}=y();return ue(f),(e,t)=>(r(),l(M,v(u(c),{ref:u(d),"trap-focus":u(o).open.value,"disable-outside-pointer-events":``,onCloseAutoFocus:t[0]||=g(e=>{i(`closeAutoFocus`,e),s.value||u(o).triggerElement.value?.focus()},[`prevent`]),onPointerDownOutside:t[1]||=e=>{i(`pointerDownOutside`,e);let t=e.detail.originalEvent,n=t.button===0&&t.ctrlKey===!0,r=t.button===2||n;s.value=r},onFocusOutside:t[2]||=g(()=>{},[`prevent`])}),{default:m(()=>[a(e.$slots,`default`)]),_:3},16,[`trap-focus`]))}})})))()}var I;function L(){return(L=e((()=>{w(),j(),N(),f(),I=p({__name:`PopoverContentNonModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,o=O(),s=_(!1),c=_(!1),d=T(n,i);return(e,t)=>(r(),l(M,v(u(d),{"trap-focus":!1,"disable-outside-pointer-events":!1,onCloseAutoFocus:t[0]||=e=>{i(`closeAutoFocus`,e),e.defaultPrevented||(s.value||u(o).triggerElement.value?.focus(),e.preventDefault()),s.value=!1,c.value=!1},onInteractOutside:t[1]||=async e=>{i(`interactOutside`,e),e.defaultPrevented||(s.value=!0,e.detail.originalEvent.type===`pointerdown`&&(c.value=!0));let t=e.target;u(o).triggerElement.value?.contains(t)&&e.preventDefault(),e.detail.originalEvent.type===`focusin`&&c.value&&e.preventDefault()}}),{default:m(()=>[a(e.$slots,`default`)]),_:3},16))}})})))()}var R;function z(){return(z=e((()=>{b(),w(),C(),Te(),j(),F(),L(),f(),R=p({__name:`PopoverContent`,props:{forceMount:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,i=t,o=O(),s=T(n,i),{forwardRef:c}=y();return o.contentId||=S(void 0,`reka-popover-content`),(e,t)=>(r(),l(u(Ee),{present:e.forceMount||u(o).open.value},{default:m(()=>[u(o).modal.value?(r(),l(P,v({key:0},u(s),{ref:u(c)}),{default:m(()=>[a(e.$slots,`default`)]),_:3},16)):(r(),l(I,v({key:1},u(s),{ref:u(c)}),{default:m(()=>[a(e.$slots,`default`)]),_:3},16))]),_:3},8,[`present`]))}})})))()}var B;function V(){return(V=e((()=>{E(),f(),B=p({__name:`PopoverPortal`,props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(e){let t=e;return(e,n)=>(r(),l(u(ke),te(o(t)),{default:m(()=>[a(e.$slots,`default`)]),_:3},16))}})})))()}var H;function U(){return(U=e((()=>{b(),C(),ce(),Se(),j(),f(),H=p({__name:`PopoverTrigger`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`}},setup(e){let n=e,o=O(),{forwardRef:s,currentElement:c}=y();return o.triggerId||=S(void 0,`reka-popover-trigger`),i(()=>{o.triggerElement.value=c.value}),(e,i)=>(r(),l(d(u(o).hasCustomAnchor.value?u(x):u(_e)),{"as-child":``},{default:m(()=>[t(u(x),{id:u(o).triggerId,ref:u(s),type:e.as===`button`?`button`:void 0,"aria-haspopup":`dialog`,"aria-expanded":u(o).open.value,"aria-controls":u(o).contentId,"data-state":u(o).open.value?`open`:`closed`,as:e.as,"as-child":n.asChild,onClick:u(o).onOpenToggle},{default:m(()=>[a(e.$slots,`default`)]),_:3},8,[`id`,`type`,`aria-expanded`,`aria-controls`,`data-state`,`as`,`as-child`,`onClick`])]),_:3}))}})})))()}var W;function G(){return(G=e((()=>{f(),z(),V(),j(),U(),W=p({inheritAttrs:!1,__name:`CspPopover`,props:s({side:{default:`bottom`},align:{default:`start`}},{open:{type:Boolean},openModifiers:{}}),emits:[`update:open`],setup(e){let i=ee(e,`open`),o=!!h().trigger;return(s,c)=>(r(),l(u(A),{open:i.value,"onUpdate:open":c[0]||=e=>i.value=e},{default:m(()=>[u(o)?(r(),l(u(H),{key:0,"as-child":``},{default:m(()=>[a(s.$slots,`trigger`)]),_:3})):n(``,!0),t(u(B),null,{default:m(()=>[t(u(R),{class:`csp-popover`,side:e.side,align:e.align,"side-offset":6},{default:m(()=>[a(s.$slots,`default`)]),_:3},8,[`side`,`align`])]),_:3})]),_:3},8,[`open`]))}})})))()}var K;function q(){return(q=e((()=>{G(),K=W,W.__docgenInfo=Object.assign({displayName:W.name??W.__name},{exportName:`default`,displayName:`CspPopover`,type:1,props:[{name:`side`,global:!1,default:`"bottom"`,description:``,tags:[],required:!1,type:`"top" | "right" | "bottom" | "left" | undefined`,schema:{kind:`enum`,type:`"top" | "right" | "bottom" | "left" | undefined`,schema:[`undefined`,`"top"`,`"right"`,`"bottom"`,`"left"`]},declarations:[]},{name:`align`,global:!1,default:`"start"`,description:``,tags:[],required:!1,type:`"end" | "start" | "center" | undefined`,schema:{kind:`enum`,type:`"end" | "start" | "center" | undefined`,schema:[`undefined`,`"end"`,`"start"`,`"center"`]},declarations:[]},{name:`open`,global:!1,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean | undefined]`,signature:`(event: "update:open", value: boolean | undefined): void`,schema:[{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]}],declarations:[]}],slots:[{name:`trigger`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspPopover/CspPopover.vue`})})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{Ae(),q(),Me(),J={title:`Éléments/Génériques/CspPopover`,component:K,tags:[`autodocs`],parameters:{controls:{include:[`open`,`side`,`align`]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:`centered`},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Côté d'apparition du popover.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`bottom`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du popover par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:`bottom`,align:`start`},render:e=>({components:{CspPopover:K,CspButton:D},setup(){let{controlledOpen:t,handleUpdateOpen:n,open:r}=je(e);return{args:e,controlledOpen:t,handleUpdateOpen:n,open:r}},template:`
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
    `})},Q=[`Default`,`Sides`,`Alignments`],Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}}})))()}$();export{Z as Alignments,Y as Default,X as Sides,Q as __namedExportsOrder,J as default};