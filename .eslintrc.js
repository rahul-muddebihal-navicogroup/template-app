module.exports = {
  root: true,
  env: {
    es6: true,
    'react-native/react-native': true,
  },
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    sourceType: 'module',
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    '@react-native-community',
    'plugin:@typescript-eslint/recommended',
    'prettier/@typescript-eslint',
    'prettier',
  ],
  rules: {
    'prettier/prettier': 'error',
    'react-hooks/rules-of-hooks': 'error', // if using hooks
    'react-hooks/exhaustive-deps': 'warn', // if using hooks,
    '@typescript-eslint/explicit-module-boundary-types': 'off', // Require explicit return and argument types on exported functions,
    'react-native/no-inline-styles': 'off', // inline styles,
    'no-shadow': 'off',
    '@typescript-eslint/no-explicit-any': 'off', // implicit any
  },
  plugins: ['react', 'react-hooks', 'react-native', '@typescript-eslint', 'prettier'],
};
