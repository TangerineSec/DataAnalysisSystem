# front

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### 使用方法：
```
set NODE_OPTIONS=--openssl-legacy-provider
npm run serve
```
"scripts": {
   "dev": "webpack-dev-server --disableHostCheck=true --line --progress --config build/webpack.dev.conf.js",