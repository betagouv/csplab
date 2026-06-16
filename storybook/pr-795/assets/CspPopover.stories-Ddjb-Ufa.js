import{C as S}from"./CspButton-DdZRQonE.js";import{l as y,_ as z,K as c,f as m,ab as d,Q as g,a1 as e,O as q,j as P,y as h,ae as A,B as G,p as W,G as H,R as Q,a4 as J,a5 as X,x as Y,g as Z}from"./vue.esm-bundler-7zVN4DZj.js";import{q as ee,a as te,r as oe,l as F}from"./useForwardExpose-qwf_wVRM.js";import{c as re,u as ae,b as se,d as D,P as ne}from"./PopperContent-DMAzS00b.js";import{u as K}from"./useId-Blg3GNwK.js";import{P as le}from"./Presence-CGGvXRHO.js";import{F as ie,u as pe,a as ue}from"./FocusScope-kJbVssvv.js";import{u as de}from"./useFocusGuards-lofhKZlc.js";import{D as fe,T as ce}from"./Teleport-D2JxKccQ.js";import{P as N}from"./Primitive-DzgJnGz8.js";import{u as me}from"./useStoryOpenState-Dt1ghQp-.js";import"./CspIcon-ClPxlQGO.js";import"./iconify-DRloO12f.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";import"./ConfigProvider-lmrMonQJ.js";import"./nullish-CHIgUVhi.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";const[_,ge]=te("PopoverRoot");var ve=y({__name:"PopoverRoot",props:{defaultOpen:{type:Boolean,required:!1,default:!1},open:{type:Boolean,required:!1,default:void 0},modal:{type:Boolean,required:!1,default:!1}},emits:["update:open"],setup(a,{emit:n}){const t=a,o=n,{modal:l}=z(t),r=ee(t,"open",o,{defaultValue:t.defaultOpen,passive:t.open===void 0}),p=q(),f=q(!1);return ge({contentId:"",triggerId:"",modal:l,open:r,onOpenChange:s=>{r.value=s},onOpenToggle:()=>{r.value=!r.value},triggerElement:p,hasCustomAnchor:f}),(s,i)=>(c(),m(e(re),null,{default:d(()=>[g(s.$slots,"default",{open:e(r),close:()=>r.value=!1})]),_:3}))}}),ye=ve,be=y({__name:"PopoverContentImpl",props:{trapFocus:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:["escapeKeyDown","pointerDownOutside","focusOutside","interactOutside","openAutoFocus","closeAutoFocus"],setup(a,{emit:n}){const t=a,o=n,l=ae(oe(t,"trapFocus","disableOutsidePointerEvents")),{forwardRef:r}=F(),p=_();return de(),(f,s)=>(c(),m(e(ie),{"as-child":"",loop:"",trapped:f.trapFocus,onMountAutoFocus:s[5]||(s[5]=i=>o("openAutoFocus",i)),onUnmountAutoFocus:s[6]||(s[6]=i=>o("closeAutoFocus",i))},{default:d(()=>[P(e(fe),{"as-child":"","disable-outside-pointer-events":f.disableOutsidePointerEvents,onPointerDownOutside:s[0]||(s[0]=i=>o("pointerDownOutside",i)),onInteractOutside:s[1]||(s[1]=i=>o("interactOutside",i)),onEscapeKeyDown:s[2]||(s[2]=i=>o("escapeKeyDown",i)),onFocusOutside:s[3]||(s[3]=i=>o("focusOutside",i)),onDismiss:s[4]||(s[4]=i=>e(p).onOpenChange(!1))},{default:d(()=>[P(e(se),h(e(l),{id:e(p).contentId,ref:e(r),"data-state":e(p).open.value?"open":"closed","aria-labelledby":e(p).triggerId,style:{"--reka-popover-content-transform-origin":"var(--reka-popper-transform-origin)","--reka-popover-content-available-width":"var(--reka-popper-available-width)","--reka-popover-content-available-height":"var(--reka-popper-available-height)","--reka-popover-trigger-width":"var(--reka-popper-anchor-width)","--reka-popover-trigger-height":"var(--reka-popper-anchor-height)"},role:"dialog"}),{default:d(()=>[g(f.$slots,"default")]),_:3},16,["id","data-state","aria-labelledby"])]),_:3},8,["disable-outside-pointer-events"])]),_:3},8,["trapped"]))}}),U=be,qe=y({__name:"PopoverContentModal",props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:["escapeKeyDown","pointerDownOutside","focusOutside","interactOutside","openAutoFocus","closeAutoFocus"],setup(a,{emit:n}){const t=a,o=n,l=_(),r=q(!1);pe(!0);const p=D(t,o),{forwardRef:f,currentElement:s}=F();return ue(s),(i,u)=>(c(),m(U,h(e(p),{ref:e(f),"trap-focus":e(l).open.value,"disable-outside-pointer-events":"",onCloseAutoFocus:u[0]||(u[0]=A(v=>{var b;o("closeAutoFocus",v),r.value||(b=e(l).triggerElement.value)==null||b.focus()},["prevent"])),onPointerDownOutside:u[1]||(u[1]=v=>{o("pointerDownOutside",v);const b=v.detail.originalEvent,O=b.button===0&&b.ctrlKey===!0,V=b.button===2||O;r.value=V}),onFocusOutside:u[2]||(u[2]=A(()=>{},["prevent"]))}),{default:d(()=>[g(i.$slots,"default")]),_:3},16,["trap-focus"]))}}),Pe=qe,he=y({__name:"PopoverContentNonModal",props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:["escapeKeyDown","pointerDownOutside","focusOutside","interactOutside","openAutoFocus","closeAutoFocus"],setup(a,{emit:n}){const t=a,o=n,l=_(),r=q(!1),p=q(!1),f=D(t,o);return(s,i)=>(c(),m(U,h(e(f),{"trap-focus":!1,"disable-outside-pointer-events":!1,onCloseAutoFocus:i[0]||(i[0]=u=>{var v;o("closeAutoFocus",u),u.defaultPrevented||(r.value||(v=e(l).triggerElement.value)==null||v.focus(),u.preventDefault()),r.value=!1,p.value=!1}),onInteractOutside:i[1]||(i[1]=async u=>{var O;o("interactOutside",u),u.defaultPrevented||(r.value=!0,u.detail.originalEvent.type==="pointerdown"&&(p.value=!0));const v=u.target;((O=e(l).triggerElement.value)==null?void 0:O.contains(v))&&u.preventDefault(),u.detail.originalEvent.type==="focusin"&&p.value&&u.preventDefault()})}),{default:d(()=>[g(s.$slots,"default")]),_:3},16))}}),Ce=he,_e=y({__name:"PopoverContent",props:{forceMount:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:["escapeKeyDown","pointerDownOutside","focusOutside","interactOutside","openAutoFocus","closeAutoFocus"],setup(a,{emit:n}){const t=a,o=n,l=_(),r=D(t,o),{forwardRef:p}=F();return l.contentId||(l.contentId=K(void 0,"reka-popover-content")),(f,s)=>(c(),m(e(le),{present:f.forceMount||e(l).open.value},{default:d(()=>[e(l).modal.value?(c(),m(Pe,h({key:0},e(r),{ref:e(p)}),{default:d(()=>[g(f.$slots,"default")]),_:3},16)):(c(),m(Ce,h({key:1},e(r),{ref:e(p)}),{default:d(()=>[g(f.$slots,"default")]),_:3},16))]),_:3},8,["present"]))}}),Oe=_e,Be=y({__name:"PopoverPortal",props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(a){const n=a;return(t,o)=>(c(),m(e(ce),G(W(n)),{default:d(()=>[g(t.$slots,"default")]),_:3},16))}}),ke=Be,we=y({__name:"PopoverTrigger",props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:"button"}},setup(a){const n=a,t=_(),{forwardRef:o,currentElement:l}=F();return t.triggerId||(t.triggerId=K(void 0,"reka-popover-trigger")),H(()=>{t.triggerElement.value=l.value}),(r,p)=>(c(),m(Q(e(t).hasCustomAnchor.value?e(N):e(ne)),{"as-child":""},{default:d(()=>[P(e(N),{id:e(t).triggerId,ref:e(o),type:r.as==="button"?"button":void 0,"aria-haspopup":"dialog","aria-expanded":e(t).open.value,"aria-controls":e(t).contentId,"data-state":e(t).open.value?"open":"closed",as:r.as,"as-child":n.asChild,onClick:e(t).onOpenToggle},{default:d(()=>[g(r.$slots,"default")]),_:3},8,["id","type","aria-expanded","aria-controls","data-state","as","as-child","onClick"])]),_:3}))}}),Fe=we;const C=y({inheritAttrs:!1,__name:"CspPopover",props:Y({side:{default:"bottom"},align:{default:"start"}},{open:{type:Boolean},openModifiers:{}}),emits:["update:open"],setup(a){const n=J(a,"open"),o=!!X().trigger;return(l,r)=>(c(),m(e(ye),{open:n.value,"onUpdate:open":r[0]||(r[0]=p=>n.value=p)},{default:d(()=>[e(o)?(c(),m(e(Fe),{key:0,"as-child":""},{default:d(()=>[g(l.$slots,"trigger")]),_:3})):Z("",!0),P(e(ke),null,{default:d(()=>[P(e(Oe),{class:"csp-popover",side:a.side,align:a.align,"side-offset":6},{default:d(()=>[g(l.$slots,"default")]),_:3},8,["side","align"])]),_:3})]),_:3},8,["open"]))}});C.__docgenInfo={exportName:"default",displayName:"CspPopover",type:1,props:[{name:"side",global:!1,description:"",tags:[],required:!1,type:'"bottom" | "top" | "right" | "left"',declarations:[],schema:{kind:"enum",type:'"bottom" | "top" | "right" | "left"',schema:['"bottom"','"top"','"right"','"left"']},default:'"bottom"'},{name:"align",global:!1,description:"",tags:[],required:!1,type:'"start" | "center" | "end"',declarations:[],schema:{kind:"enum",type:'"start" | "center" | "end"',schema:['"start"','"center"','"end"']},default:'"start"'},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"open",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}}],events:[{name:"update:open",description:"",tags:[],type:"[value: boolean]",signature:'(event: "update:open", value: boolean): void',declarations:[],schema:[{kind:"enum",type:"boolean",schema:["false","true"]}]}],slots:[{name:"trigger",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"default",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}}],exposed:[{name:"side",type:'"bottom" | "top" | "right" | "left"',description:"",declarations:[],schema:{kind:"enum",type:'"bottom" | "top" | "right" | "left"',schema:['"bottom"','"top"','"right"','"left"']}},{name:"align",type:'"start" | "center" | "end"',description:"",declarations:[],schema:{kind:"enum",type:'"start" | "center" | "end"',schema:['"start"','"center"','"end"']}},{name:"open",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspPopover/CspPopover.vue"};const Ge={title:"Éléments/Génériques/CspPopover",component:C,tags:["autodocs"],parameters:{controls:{include:["open","side","align"]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:"centered"},argTypes:{open:{control:{type:"boolean"},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:"boolean"}}},side:{control:{type:"radio"},options:["top","right","bottom","left"],description:"Côté d'apparition du popover.",table:{type:{summary:"top | right | bottom | left"},defaultValue:{summary:"bottom"}}},align:{control:{type:"radio"},options:["start","center","end"],description:"Alignement du popover par rapport au déclencheur.",table:{type:{summary:"start | center | end"},defaultValue:{summary:"start"}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:"bottom",align:"start"},render:a=>({components:{CspPopover:C,CspButton:S},setup(){const{controlledOpen:n,handleUpdateOpen:t,open:o}=me(a);return{args:a,controlledOpen:n,handleUpdateOpen:t,open:o}},template:`
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
    `})},B={name:"Par défaut"},k={name:"Côtés",render:a=>({components:{CspPopover:C,CspButton:S},setup(){return{args:a,sides:[{label:"Haut",value:"top"},{label:"Droite",value:"right"},{label:"Bas",value:"bottom"},{label:"Gauche",value:"left"}]}},template:`
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
    `})},w={name:"Alignements",render:a=>({components:{CspPopover:C,CspButton:S},setup(){return{args:a,alignments:[{label:"Début",value:"start"},{label:"Centre",value:"center"},{label:"Fin",value:"end"}]}},template:`
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
    `})};var E,R,I;B.parameters={...B.parameters,docs:{...(E=B.parameters)==null?void 0:E.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...(I=(R=B.parameters)==null?void 0:R.docs)==null?void 0:I.source}}};var M,L,j;k.parameters={...k.parameters,docs:{...(M=k.parameters)==null?void 0:M.docs,source:{originalSource:`{
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
}`,...(j=(L=k.parameters)==null?void 0:L.docs)==null?void 0:j.source}}};var x,T,$;w.parameters={...w.parameters,docs:{...(x=w.parameters)==null?void 0:x.docs,source:{originalSource:`{
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
}`,...($=(T=w.parameters)==null?void 0:T.docs)==null?void 0:$.source}}};const We=["Default","Sides","Alignments"];export{w as Alignments,B as Default,k as Sides,We as __namedExportsOrder,Ge as default};
