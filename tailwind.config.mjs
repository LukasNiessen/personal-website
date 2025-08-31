import defaultTheme from 'tailwindcss/defaultTheme';

/** @type {import('tailwindcss').Config} */
export default {
	darkMode: ['class'],
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				warmBg: {
					light: '#ffffff', // Pure white for modern clean look
					dark: '#0a0a0a', // Modern dark like xAI/Cursor
				},
				warmAccent: {
					primary: '#66b9ff', // Blue from VANTA fog midtone
					secondary: '#1c99e3', // Highlight blue from VANTA
					tertiary: '#832d84', // Purple from VANTA lowlight
				},
				warmText: {
					light: '#171717', // Modern dark text for light mode
					dark: '#e5e5e5', // Clean light text for dark mode
				},
			},
			fontFamily: {
				sans: ['Atkinson', ...defaultTheme.fontFamily.sans],
			},
			typography: {
				DEFAULT: {
					css: {
						maxWidth: 'full',
						a: {
							overflowWrap: 'break-word',
							wordWrap: 'break-word',
							wordBreak: 'break-word',
							hyphens: 'auto',
						},
					},
				},
			},
			rotate: {
				45: '45deg',
				135: '135deg',
				225: '225deg',
				315: '315deg',
			},
			animation: {
				twinkle: 'twinkle 2s ease-in-out forwards',
				meteor: 'meteor 3s ease-in-out forwards',
			},
			keyframes: {
				twinkle: {
					'0%': {
						opacity: 0,
						transform: 'rotate(0deg)',
					},
					'50%': {
						opacity: 1,
						transform: 'rotate(180deg)',
					},
					'100%': {
						opacity: 0,
						transform: 'rotate(360deg)',
					},
				},
				meteor: {
					'0%': {
						opacity: 0,
						transform: 'translateY(200%)',
					},
					'50%': {
						opacity: 1,
					},
					'100%': {
						opacity: 0,
						transform: 'translateY(0)',
					},
				},
			},
		},
	},
	plugins: [require('@tailwindcss/typography')],
};
