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
      loading: false,
    }
  },
  methods: {
    async onSubmit() {
      // try {
      //   let response = await this.$auth.loginWith('local', {data: {username: this.login, password: this.password}})
      //   console.log(response)
      // } catch (err) {
      //   console.log(err)
      // }
      this.loading = true
      this.$store.dispatch("authorization/postAuth", {username: this.login, password: this.password})
        .then(res => {
          if (res.detail) {
            this.$buefy.toast.open({
              message: res.detail,
              type: 'is-danger'
            })
          }
        })
      .catch(e=> {
        this.$buefy.toast.open({
          message: e,
          type: 'is-danger'
        })
      })
      .finally(()=>{
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.login__form {
  min-width: 400px;
  margin-top: 15%;
}
</style>
