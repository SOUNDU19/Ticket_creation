# NexoraAI UI Design System

## Dark Glassmorphism Theme

The application now features a stunning dark glassmorphism design inspired by modern UI trends, with floating gradient orbs and frosted glass effects.

## Color Palette

### Primary Colors
- **Primary Purple**: `#a855f7` - Main brand color
- **Primary Dark**: `#7e22ce` - Darker purple variant
- **Primary Light**: `#c084fc` - Lighter purple variant

### Secondary Colors
- **Secondary Orange**: `#f97316` - Accent color
- **Secondary Dark**: `#ea580c` - Darker orange
- **Secondary Light**: `#fb923c` - Lighter orange

### Accent Colors
- **Pink Accent**: `#ec4899` - Additional accent
- **Success Green**: `#10b981` - Success states
- **Warning Yellow**: `#f59e0b` - Warning states
- **Danger Red**: `#ef4444` - Error states

### Background Colors
- **Dark Base**: `#0a0a0a` - Main background
- **Dark Light**: `#1a1a1a` - Secondary background
- **Dark Card**: `#1f1f1f` - Card backgrounds

## Key Design Features

### 1. Floating Gradient Orbs
- Large blurred gradient spheres that float in the background
- Purple and orange color scheme
- Smooth animations with 20-30 second cycles
- Mouse interaction for dynamic movement
- Creates depth and visual interest

### 2. Glassmorphism Effects
- Frosted glass cards with `backdrop-filter: blur(20px)`
- Semi-transparent backgrounds `rgba(31, 31, 31, 0.7)`
- Subtle borders `rgba(255, 255, 255, 0.1)`
- Layered depth with shadows and insets

### 3. Gradient Accents
- Purple to orange gradients on buttons
- Gradient text effects on headings
- Gradient borders on interactive elements
- Smooth color transitions

### 4. Interactive Elements
- Hover effects with scale and lift
- Ripple effects on button clicks
- Smooth transitions (0.3s cubic-bezier)
- Glow effects on focus states

## Component Styles

### Buttons
```css
.btn-primary {
  background: linear-gradient(135deg, #a855f7, #f97316);
  box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
  border-radius: 12px;
}
```

### Cards
```css
.card {
  background: rgba(31, 31, 31, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}
```

### Form Inputs
```css
.form-input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}
```

## Typography

### Font Family
- **Primary**: Inter (Google Fonts)
- **Fallback**: -apple-system, BlinkMacSystemFont, sans-serif

### Font Sizes
- **Hero H1**: 4rem (64px)
- **Section H2**: 2.5rem (40px)
- **Card Title**: 1.25rem (20px)
- **Body Text**: 0.95rem (15.2px)
- **Small Text**: 0.8rem (12.8px)

### Font Weights
- **Light**: 300
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700
- **Extrabold**: 800
- **Black**: 900

## Spacing System

### Padding
- **Small**: 0.875rem (14px)
- **Medium**: 1.75rem (28px)
- **Large**: 2.5rem (40px)

### Margins
- **Section Gap**: 4rem (64px)
- **Card Gap**: 1.5rem (24px)
- **Element Gap**: 1rem (16px)

### Border Radius
- **Small**: 8px
- **Medium**: 12px
- **Large**: 16px
- **XLarge**: 20px
- **XXLarge**: 24px

## Animation System

### Keyframes

#### Float Animation
```css
@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(50px, -50px) scale(1.1); }
  66% { transform: translate(-30px, 30px) scale(0.9); }
}
```

#### Slide In Right
```css
@keyframes slideInRight {
  from { transform: translateX(400px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
```

#### Ripple Effect
```css
@keyframes ripple {
  to { transform: scale(2); opacity: 0; }
}
```

### Transition Timing
- **Fast**: 0.2s ease
- **Standard**: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- **Slow**: 0.4s cubic-bezier(0.4, 0, 0.2, 1)

## Responsive Breakpoints

### Mobile
- **Max Width**: 768px
- Single column layouts
- Collapsed navigation
- Reduced font sizes
- Smaller padding

### Tablet
- **Min Width**: 769px
- **Max Width**: 1024px
- Two column grids
- Medium spacing

### Desktop
- **Min Width**: 1025px
- Multi-column layouts
- Full navigation
- Maximum spacing

## Accessibility

### Contrast Ratios
- Text on dark background: 15:1 (AAA)
- Interactive elements: Clear focus states
- Color-blind friendly palette

### Focus States
- Visible outline on keyboard navigation
- Glow effects on form inputs
- Scale effects on buttons

### Screen Reader Support
- Semantic HTML structure
- ARIA labels where needed
- Proper heading hierarchy

## Implementation Notes

### Particles System
- Implemented in `js/particles.js`
- Creates 5 floating orbs
- Mouse interaction enabled
- Performance optimized with CSS animations

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Backdrop-filter support required
- CSS Grid and Flexbox
- CSS Custom Properties (variables)

### Performance
- Hardware-accelerated animations
- Optimized blur filters
- Lazy loading for images
- Minimal JavaScript overhead

## Page-Specific Styles

### Auth Pages (Login/Signup)
- Centered card layout
- Maximum width: 450px
- Prominent floating orbs
- Clean, minimal design

### Dashboard
- Stats grid layout
- Gradient stat icons
- Recent activity section
- Quick action buttons

### Landing Page
- Hero section with large text
- Feature cards grid
- How it works section
- Pricing tables
- Footer with credits

## Best Practices

1. **Consistency**: Use design tokens (CSS variables) throughout
2. **Hierarchy**: Clear visual hierarchy with size and color
3. **Spacing**: Consistent spacing using the spacing system
4. **Feedback**: Visual feedback on all interactions
5. **Performance**: Optimize animations and effects
6. **Accessibility**: Maintain WCAG AA standards minimum

## Future Enhancements

- [ ] Dark/Light mode toggle
- [ ] Custom theme builder
- [ ] More animation presets
- [ ] Advanced particle effects
- [ ] Micro-interactions
- [ ] Loading skeletons
- [ ] Toast notification system
- [ ] Modal animations

---

**Design Credits**: Inspired by modern glassmorphism trends and premium SaaS applications
**Developed by**: Soundarya
