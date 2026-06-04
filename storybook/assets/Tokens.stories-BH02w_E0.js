const z={title:"Fondations/Tokens",parameters:{docs:{description:{component:`Catalogue visuel des tokens DSFR + extensions CSPLab.

`}}}},u=[{group:"Texte",tokens:["--text-default-grey","--text-title-grey","--text-title-blue-france","--text-action-high-blue-france","--text-action-high-grey","--text-mention-grey","--text-disabled-grey","--text-inverted-grey","--text-default-info","--text-default-success","--text-default-warning","--text-default-error"]},{group:"Fonds",tokens:["--background-default-grey","--background-alt-grey","--background-alt-blue-france","--background-contrast-grey","--background-elevated-grey","--background-contrast-info","--background-contrast-success","--background-contrast-warning","--background-contrast-error","--background-action-high-blue-france","--background-action-high-blue-france-hover","--background-action-high-blue-france-active","--background-action-high-red-marianne","--background-action-high-red-marianne-hover","--background-action-high-red-marianne-active","--background-default-grey-hover","--background-default-grey-active","--background-disabled-grey"]},{group:"Bordures",tokens:["--border-default-grey","--border-default-blue-france","--border-action-high-blue-france","--border-plain-info","--border-plain-success","--border-plain-warning","--border-plain-error","--border-disabled-grey","--csp-focus-ring-color"]}],x=["--csp-space-1","--csp-space-2","--csp-space-3","--csp-space-4","--csp-space-5","--csp-space-6","--csp-space-8","--csp-space-10","--csp-space-12","--csp-space-16"],m=[{token:"--csp-font-size-xs",label:"xs — caption"},{token:"--csp-font-size-sm",label:"sm — meta / chip"},{token:"--csp-font-size-base",label:"base — body"},{token:"--csp-font-size-md",label:"md — body fort"},{token:"--csp-font-size-lg",label:"lg — sous-titre"},{token:"--csp-font-size-xl",label:"xl — titre section"},{token:"--csp-font-size-2xl",label:"2xl — titre page"}],b=[{token:"--csp-font-weight-regular",label:"regular | 400"},{token:"--csp-font-weight-medium",label:"medium | 500"},{token:"--csp-font-weight-bold",label:"bold | 700"}],h=[{token:"--csp-line-height-tight",label:"tight | 1.25"},{token:"--csp-line-height-base",label:"base | 1.5"},{token:"--csp-line-height-relaxed",label:"relaxed | 1.625"}],k=["--csp-shadow-sm","--csp-shadow-md","--csp-shadow-lg"],e={render:()=>({setup:()=>({groups:u}),template:`
      <div style="padding: var(--csp-space-6); display: flex; flex-direction: column; gap: var(--csp-space-8);">
        <section v-for="g in groups" :key="g.group">
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">{{ g.group }}</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: var(--csp-space-3);">
            <div v-for="t in g.tokens" :key="t" style="border: 1px solid var(--border-default-grey); border-radius: var(--csp-radius-md); overflow: hidden;">
              <div :style="{ background: 'var(' + t + ')', height: '56px' }"></div>
              <div style="padding: var(--csp-space-2); font-family: ui-monospace, monospace; font-size: var(--csp-font-size-xs); color: var(--text-mention-grey); background: var(--background-default-grey);">{{ t }}</div>
            </div>
          </div>
        </section>
      </div>
    `})},t={render:()=>({setup:()=>({tokens:x}),template:`
      <div style="padding: var(--csp-space-6); display: flex; flex-direction: column; gap: var(--csp-space-3);">
        <div v-for="t in tokens" :key="t" style="display: flex; align-items: center; gap: var(--csp-space-4);">
          <code style="width: 220px; font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t }}</code>
          <div :style="{ width: 'var(' + t + ')', height: '20px', background: 'var(--background-action-high-blue-france)', borderRadius: '2px' }"></div>
        </div>
      </div>
    `})},s={render:()=>({setup:()=>({fontSizes:m,fontWeights:b,lineHeights:h}),template:`
      <div style="padding: var(--csp-space-6); display: flex; flex-direction: column; gap: var(--csp-space-8);">
        <section>
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">Tailles</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csp-space-4);">
            <div v-for="t in fontSizes" :key="t.token" style="display: flex; align-items: baseline; gap: var(--csp-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csp-space-2);">
              <span :style="{ fontSize: 'var(' + t.token + ')', color: 'var(--text-title-grey)', minWidth: '280px' }">{{ t.label }}</span>
              <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
        <section>
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">Graisses</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csp-space-4);">
            <div v-for="t in fontWeights" :key="t.token" style="display: flex; align-items: baseline; gap: var(--csp-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csp-space-2);">
              <span :style="{ fontWeight: 'var(' + t.token + ')', fontSize: 'var(--csp-font-size-md)', color: 'var(--text-title-grey)', minWidth: '280px' }">{{ t.label }}</span>
              <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
        <section>
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">Hauteurs de ligne</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csp-space-4);">
            <div v-for="t in lineHeights" :key="t.token" style="display: flex; align-items: flex-start; gap: var(--csp-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csp-space-2);">
              <p :style="{ lineHeight: 'var(' + t.token + ')', fontSize: 'var(--csp-font-size-sm)', color: 'var(--text-title-grey)', minWidth: '280px', margin: 0 }">{{ t.label }}<br>Texte exemple sur deux lignes<br>pour visualiser l'interligne</p>
              <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
      </div>
    `})},a={render:()=>({setup:()=>({tokens:k}),template:`
      <div style="padding: var(--csp-space-8); display: flex; gap: var(--csp-space-8); background: var(--background-alt-grey);">
        <div v-for="t in tokens" :key="t" style="text-align: center;">
          <div :style="{ width: '160px', height: '100px', background: 'var(--background-default-grey)', borderRadius: 'var(--csp-radius-md)', boxShadow: 'var(' + t + ')', marginBottom: 'var(--csp-space-3)' }"></div>
          <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t }}</code>
        </div>
      </div>
    `})};var r,o,i;e.parameters={...e.parameters,docs:{...(r=e.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => ({
    setup: () => ({
      groups: COLOR_GROUPS
    }),
    template: \`
      <div style="padding: var(--csp-space-6); display: flex; flex-direction: column; gap: var(--csp-space-8);">
        <section v-for="g in groups" :key="g.group">
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">{{ g.group }}</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: var(--csp-space-3);">
            <div v-for="t in g.tokens" :key="t" style="border: 1px solid var(--border-default-grey); border-radius: var(--csp-radius-md); overflow: hidden;">
              <div :style="{ background: 'var(' + t + ')', height: '56px' }"></div>
              <div style="padding: var(--csp-space-2); font-family: ui-monospace, monospace; font-size: var(--csp-font-size-xs); color: var(--text-mention-grey); background: var(--background-default-grey);">{{ t }}</div>
            </div>
          </div>
        </section>
      </div>
    \`
  })
}`,...(i=(o=e.parameters)==null?void 0:o.docs)==null?void 0:i.source}}};var n,c,l;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => ({
    setup: () => ({
      tokens: SPACING_TOKENS
    }),
    template: \`
      <div style="padding: var(--csp-space-6); display: flex; flex-direction: column; gap: var(--csp-space-3);">
        <div v-for="t in tokens" :key="t" style="display: flex; align-items: center; gap: var(--csp-space-4);">
          <code style="width: 220px; font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t }}</code>
          <div :style="{ width: 'var(' + t + ')', height: '20px', background: 'var(--background-action-high-blue-france)', borderRadius: '2px' }"></div>
        </div>
      </div>
    \`
  })
}`,...(l=(c=t.parameters)==null?void 0:c.docs)==null?void 0:l.source}}};var d,p,g;s.parameters={...s.parameters,docs:{...(d=s.parameters)==null?void 0:d.docs,source:{originalSource:`{
  render: () => ({
    setup: () => ({
      fontSizes: FONT_SIZE_TOKENS,
      fontWeights: FONT_WEIGHT_TOKENS,
      lineHeights: LINE_HEIGHT_TOKENS
    }),
    template: \`
      <div style="padding: var(--csp-space-6); display: flex; flex-direction: column; gap: var(--csp-space-8);">
        <section>
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">Tailles</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csp-space-4);">
            <div v-for="t in fontSizes" :key="t.token" style="display: flex; align-items: baseline; gap: var(--csp-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csp-space-2);">
              <span :style="{ fontSize: 'var(' + t.token + ')', color: 'var(--text-title-grey)', minWidth: '280px' }">{{ t.label }}</span>
              <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
        <section>
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">Graisses</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csp-space-4);">
            <div v-for="t in fontWeights" :key="t.token" style="display: flex; align-items: baseline; gap: var(--csp-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csp-space-2);">
              <span :style="{ fontWeight: 'var(' + t.token + ')', fontSize: 'var(--csp-font-size-md)', color: 'var(--text-title-grey)', minWidth: '280px' }">{{ t.label }}</span>
              <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
        <section>
          <h3 style="margin: 0 0 var(--csp-space-3); font-size: var(--csp-font-size-lg); color: var(--text-title-grey);">Hauteurs de ligne</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csp-space-4);">
            <div v-for="t in lineHeights" :key="t.token" style="display: flex; align-items: flex-start; gap: var(--csp-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csp-space-2);">
              <p :style="{ lineHeight: 'var(' + t.token + ')', fontSize: 'var(--csp-font-size-sm)', color: 'var(--text-title-grey)', minWidth: '280px', margin: 0 }">{{ t.label }}<br>Texte exemple sur deux lignes<br>pour visualiser l'interligne</p>
              <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
      </div>
    \`
  })
}`,...(g=(p=s.parameters)==null?void 0:p.docs)==null?void 0:g.source}}};var v,f,y;a.parameters={...a.parameters,docs:{...(v=a.parameters)==null?void 0:v.docs,source:{originalSource:`{
  render: () => ({
    setup: () => ({
      tokens: SHADOW_TOKENS
    }),
    template: \`
      <div style="padding: var(--csp-space-8); display: flex; gap: var(--csp-space-8); background: var(--background-alt-grey);">
        <div v-for="t in tokens" :key="t" style="text-align: center;">
          <div :style="{ width: '160px', height: '100px', background: 'var(--background-default-grey)', borderRadius: 'var(--csp-radius-md)', boxShadow: 'var(' + t + ')', marginBottom: 'var(--csp-space-3)' }"></div>
          <code style="font-size: var(--csp-font-size-xs); color: var(--text-mention-grey);">{{ t }}</code>
        </div>
      </div>
    \`
  })
}`,...(y=(f=a.parameters)==null?void 0:f.docs)==null?void 0:y.source}}};const S=["Couleurs","Espacements","Typographie","Ombres"];export{e as Couleurs,t as Espacements,a as Ombres,s as Typographie,S as __namedExportsOrder,z as default};
