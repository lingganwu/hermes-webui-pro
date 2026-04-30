import { darkTheme, type GlobalThemeOverrides } from 'naive-ui'

const baseOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#6366f1',
    primaryColorHover: '#818cf8',
    primaryColorPressed: '#4f46e5',
    primaryColorSuppl: '#a5b4fc',
    borderRadius: '8px',
    borderRadiusSmall: '4px',
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontFamilyMono: '"JetBrains Mono", "Fira Code", "Consolas", monospace',
  },
  Button: { borderRadiusMedium: '8px' },
  Card: { borderRadius: '12px' },
  Input: { borderRadius: '8px' },
  Tag: { borderRadius: '6px' },
  Message: { borderRadius: '8px' },
}

export const lightThemeOverrides: GlobalThemeOverrides = {
  ...baseOverrides,
  common: {
    ...baseOverrides.common,
    bodyColor: '#ffffff',
    cardColor: '#ffffff',
    modalColor: '#ffffff',
    popoverColor: '#ffffff',
    tableColor: '#ffffff',
    inputColor: '#ffffff',
    actionColor: '#f5f5f5',
    dividerColor: '#e5e5e5',
    borderColor: '#e5e5e5',
    hoverColor: 'rgba(0, 0, 0, 0.04)',
    textColorBase: '#1a1a1a',
    textColor1: '#1a1a1a',
    textColor2: '#666666',
    textColor3: '#999999',
  },
  Card: { ...baseOverrides.Card, color: '#ffffff', borderColor: '#e5e5e5' },
}

export const darkThemeOverrides: GlobalThemeOverrides = {
  ...baseOverrides,
  common: {
    ...baseOverrides.common,
    bodyColor: '#0a0a0a',
    cardColor: '#141414',
    modalColor: '#1e1e1e',
    popoverColor: '#1e1e1e',
    tableColor: '#141414',
    inputColor: '#1e1e1e',
    actionColor: '#1e1e1e',
    dividerColor: '#2e2e2e',
    borderColor: '#2e2e2e',
    hoverColor: 'rgba(99, 102, 241, 0.1)',
  },
  Card: { ...baseOverrides.Card, color: '#141414', borderColor: '#2e2e2e' },
  DataTable: { thColor: '#141414', tdColor: '#0a0a0a', borderColor: '#2e2e2e' },
}

export { darkTheme }
