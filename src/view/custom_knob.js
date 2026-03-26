export default {
  template: `
    <div class="flex flex-col items-center gap-2 select-none">
      <div ref="knobRef" class="relative group"
           :class="[disable ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer']"
           :style="{ width: sizeStr, height: sizeStr }"
           @mousedown="handleMouseDown">
        
        <svg :width="sizeStr" :height="sizeStr" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" :stroke="bgStrokeColor" stroke-width="10"
                  stroke-linecap="round" :stroke-dasharray="bgDashArray"
                  stroke-dashoffset="0" transform="rotate(135 50 50)" />
          
          <circle cx="50" cy="50" r="40" fill="none" :stroke="strokeColor" stroke-width="10"
                  stroke-linecap="round" :stroke-dasharray="circumference"
                  :stroke-dashoffset="activeDashOffset" transform="rotate(135 50 50)"
                  class="transition-all duration-75 ease-out" />
        </svg>
        
        <div class="absolute top-0 left-0 w-full h-full rounded-full flex items-center justify-center transition-transform duration-75 ease-out bg-transparent"
             :style="{ transform: 'rotate(' + rotation + 'deg)' }">
           <div class="absolute top-[10%] w-1.5 h-3 bg-slate-200 rounded-full shadow-md"></div>
        </div>

        <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
          <span class="font-bold font-mono drop-shadow-md" :class="activeColorClass" :style="{ fontSize: 'calc(0.23 * ' + sizeStr + ')' }">
            {{ Number(value).toFixed(decimals) }}
          </span>
        </div>
      </div>
      
      <span v-if="label" class="text-xs font-bold text-slate-500 uppercase tracking-wider">
        {{ label }}
      </span>
    </div>
  `,
  props: {
    value: { type: Number, required: true },
    min: { type: Number, default: 0 },
    max: { type: Number, default: 100 },
    size: { type: [Number, String], default: 100 },
    color: { type: String, default: 'blue' },
    label: { type: String, default: null },
    dark_mode: { type: Boolean, default: true },
    step: { type: Number, default: 1 },
    decimals: { type: Number, default: 0 },
    disable: { type: Boolean, default: false }
  },
  data() {
    return {
      isDragging: false,
      radius: 40,
    }
  },
  computed: {
    sizeStr() { return typeof this.size === 'number' ? this.size + 'px' : this.size; },
    range() { return this.max - this.min; },
    percentage() { return Math.min(Math.max((this.value - this.min) / this.range, 0), 1); },
    rotation() { return -135 + (this.percentage * 270); },
    circumference() { return 2 * Math.PI * this.radius; },
    arcLength() { return 0.75 * this.circumference; },
    bgDashArray() { return `${this.arcLength} ${this.circumference - this.arcLength}`; },
    activeDashOffset() { return this.circumference - (this.percentage * this.arcLength); },
    activeColorClass() { return this.color === 'red' ? 'text-[#ef4444]' : 'text-[#08a4e5]'; },
    strokeColor() { return this.color === 'red' ? '#ef4444' : '#08a4e5'; },
    bgStrokeColor() { return this.dark_mode ? '#616f86ff' : '#cbd5e1'; }
  },
  methods: {
    calculateValueFromEvent(clientX, clientY) {
      if (!this.$refs.knobRef) return this.value;
      const rect = this.$refs.knobRef.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      const angleRad = Math.atan2(clientY - centerY, clientX - centerX);
      let angleDeg = (angleRad * 180) / Math.PI;
      let deg = angleDeg + 90;
      if (deg < 0) deg += 360;

      let shifted = deg - 225;
      if (shifted < 0) shifted += 360;
      let perc = shifted / 270;

      if (shifted > 270) {
        if (shifted < 315) perc = 1; else perc = 0;
      }

      let newValue = this.min + perc * this.range;
      return Math.max(this.min, Math.min(this.max, newValue));
    },
    handleMouseDown(e) {
      if (this.disable) return;
      this.isDragging = true;
      let newValue = this.calculateValueFromEvent(e.clientX, e.clientY);
      if (this.step > 0) {
        newValue = Math.round(newValue / this.step) * this.step;
      }
      newValue = Number(newValue.toFixed(this.decimals));
      this.$emit('update:value', newValue);
      document.body.style.cursor = 'grabbing';
      window.addEventListener('mousemove', this.handleMouseMove);
      window.addEventListener('mouseup', this.handleMouseUp);
    },
    handleMouseMove(e) {
      if (!this.isDragging) return;
      let newValue = this.calculateValueFromEvent(e.clientX, e.clientY);
      if (this.step > 0) {
        newValue = Math.round(newValue / this.step) * this.step;
      }
      newValue = Number(newValue.toFixed(this.decimals));
      this.$emit('update:value', newValue);
    },
    handleMouseUp() {
      this.isDragging = false;
      document.body.style.cursor = 'default';
      window.removeEventListener('mousemove', this.handleMouseMove);
      window.removeEventListener('mouseup', this.handleMouseUp);
    }
  }
};