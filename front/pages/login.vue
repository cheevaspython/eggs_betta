<template>
  <section class="section is-flex is-justify-content-center">
    <form class="box is-flex is-flex-direction-column login__form">
      <b-field label="Логин">
        <b-input v-model="login" placeholder="Введите логин" @keyup.native.enter="onSubmit"></b-input>
      </b-field>
      <b-field label="Пароль"
               :message="{'Password is too short': false, 'Password must have at least 8 characters' : false}">
        <b-input v-model="password" placeholder="Введите пароль" type="password" maxlength="30"
                 @keyup.native.enter="onSubmit"></b-input>
      </b-field>
      <div class="errorMessage" v-show="errorMessage">{{ errorMessage }}</div>
      <b-button type="is-info" @click="onSubmit" :loading="loading">Войти</b-button>
    </form>
  </section>
</template>

<script>
export default {
  name: "login",
  layout: "login",
  data() {
    return {
      login: '',
      password: '',
      errorMessage: '',
      loading: false,
    }
  },
  methods: {
    async onSubmit() {
      this.loading = true
      this.errorMessage = await this.$store.dispatch("authorization/postAuth", {username: this.login, password: this.password})
      if (this.errorMessage) {
        this.loading = false
        this.login = ''
        this.password = ''
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.login__form {
  min-width: 400px;
  margin-top: 15%;
}

.errorMessage {
  color: red;
  margin-bottom: 10px;
}
</style>
