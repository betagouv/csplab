function c(t,e,n){const s=n.originalEvent.target,a=new CustomEvent(t,{bubbles:!1,cancelable:!0,detail:n});e&&s.addEventListener(t,e,{once:!0}),s.dispatchEvent(a)}export{c as h};
