<template>
  <form action="" style="width: 1000px">
    <div class="modal-card" style="width: 900px; height: 95vh">
      <header class="modal-card-head" style="background-color: #dedede; text-align: center">
        <p class="modal-card-title" style="color: #857770; font-size: 30px; font-weight: 900">Создание заявки от продавца</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth flexbox flexbox__column">


        <div class="categories__content">
          <h1 class="categories__title">{{ trader.name }} / {{ trader.inn }}</h1>

          <div v-for="row in selectedCategories" class="flexbox__row flexbox__space-between" style="width: 100%;">
            <b-dropdown aria-role="list"  v-model="row.title">
              <template #trigger="{ active }">
                <b-field label="Категория">
                  <b-button
                  :label="row.title"
                  :icon-right="active ? 'menu-up' : 'menu-down'"
                  rounded/>
                </b-field>
              </template>
              <b-dropdown-item v-for="category in categories" aria-role="listitem" @click="changeCategory(row, category)">
                {{ category }}
              </b-dropdown-item>
            </b-dropdown>

            <b-field label="Количество (дec.)">
              <b-input v-model="row.count" type="number" rounded maxlength="10" class="mr-4"></b-input>
            </b-field>
            <b-field label="Цена ₽">
              <b-input v-model="row.price" type="float" rounded maxlength="10"></b-input>
            </b-field>
          </div>

          <b-button class="button is-success is-light mr-2" icon-left="plus" rounded @click="addRow" :disabled="addBtnDisabled">Добавить категорию</b-button>
          <b-button class="button is-success is-light" icon-left="minus" rounded @click="removeRow" :disabled="removeBtnDisabled">Убрать категорию</b-button>

          <div class="flexbox__row flexbox__space-between table">
            <div class="flexbox__column" style="padding: 10px">
              <div class="changeDates">Выберите диапазон дат</div>
              <b-datepicker
                style="width: 360px;"
                v-model="dates"
                first-day-of-week="1"
                inline
                type="is-success"
                range>
              </b-datepicker>
            </div>
            <div class="flexbox flexbox__column" style="padding: 10px; width: 423px; border-left: solid 2px #ebebeb;">
              <div class="flexbox__column" style="margin: 0 auto;">
                <b-dropdown :triggers="['hover']" aria-role="list" style="width: 100%; margin-bottom: 10px;">
                  <template #trigger>
                    <b-button
                      v-model="loading_address"  
                      label="Выберите адрес погрузки"
                      type="is-success is-light"
                      icon-right="menu-down" 
                      rounded />
                  </template>
                    
                  <b-dropdown-item v-if="prodAddress1" aria-role="listitem" @click="selectLoadingAddress(prodAddress1)">
                    <strong>{{ prodAddress1 }}</strong></b-dropdown-item>
                  <b-dropdown-item v-if="prodAddress2" aria-role="listitem" @click="selectLoadingAddress(prodAddress2)">
                    <strong>{{ prodAddress2 }}</strong></b-dropdown-item>
                  <b-dropdown-item v-if="prodAddress3" aria-role="listitem" @click="selectLoadingAddress(prodAddress3)">
                    <strong>{{ prodAddress3 }}</strong></b-dropdown-item>
                  <b-dropdown-item v-if="prodAddress4" aria-role="listitem" @click="selectLoadingAddress(prodAddress4)">
                    <strong>{{ prodAddress4 }}</strong></b-dropdown-item>
                  <b-dropdown-item v-if="prodAddress5" aria-role="listitem" @click="selectLoadingAddress(prodAddress5)">
                    <strong>{{ prodAddress5 }}</strong></b-dropdown-item>
                </b-dropdown>
              </div>
              <div class="prod-address">
                {{ loading_address }}
              </div>
              <div class="flexbox flexbox__column" style="gap: 5px;">
                <div class="bool-button" @click="isImport = !isImport" v-bind:style="{ 'background-color': getBackgroundColor(isImport) }">Импорт</div>
                <div class="flexbox__row" style="gap: 5px">
                  <div class="bool-button-half" @click="pre_payment_application = true" v-bind:style="{ 'background-color': getBackgroundColor(pre_payment_application) }">По предоплате</div>
                  <div class="bool-button-half" @click="pre_payment_application = false" v-bind:style="{ 'background-color': getBackgroundColor(!pre_payment_application) }">По постоплате</div>
                </div>
                <div class="flexbox__row flexbox__space-between input-border" v-show="!pre_payment_application" style="width: 100%; margin-top: 10px">
                <div style="margin-left: 10px; margin-top: 8px">Отсрочка оплаты</div>
                  <b-field class="my-b-input">
                    <b-input placeholder="Введите кол-во дней" rounded v-model="postponement_pay"></b-input>
                  </b-field>
                </div>
              </div>
            </div>
          </div>

          <div class="categories__comment" style="margin-top: 10px">
            <b-field label="Комментарий">
              <b-input type="textarea" v-model="comment" maxlength="255"></b-input>
            </b-field>
          </div>
        </div>

      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Создать заявку"
          :loading="loading"
          type="is-success"
          @click="sendSellerOrder"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalSellerForm",
  props: ['trader'],
  data() {
    return {
      loading: false,
      testValue: 'testv',
      isPublic: true,
      current_seller: this.trader.inn,
      cB: 0,
      cB_cost: 0,
      c0: 0,
      c0_cost: 0,
      c1: 0,
      c1_cost: 0,
      c2: 0,
      c2_cost: 0,
      c3: 0,
      c3_cost: 0,
      dirt: 0,
      dirt_cost: 0,
      dates: null,
      email: '',
      prodAddress1: this.trader.prod_address_1,
      prodAddress2: this.trader.prod_address_2,
      prodAddress3: this.trader.prod_address_3,
      prodAddress4: this.trader.prod_address_4,
      prodAddress5: this.trader.prod_address_5,
      isImport: false,
      pre_payment_application: true,
      postponement_pay: null,
      loading_address: '',
      selectedCategories: [{
        title: 'CB',
        count: 0,
        price: 0,
      }],
      comment: '',
      categories: {cB: 'CB',c0: 'C0', c1: 'C1', c2: 'C2', c3: 'C3', dirt: 'Грязь'},
      remainingCategories: {c0: 'C0',c1: 'C1', c2: 'C2', c3: 'C3', dirt: 'Грязь'}
    }
  },
  computed: {
    removeBtnDisabled() {
      return this.selectedCategories.length <= 1
    },
    addBtnDisabled() {
      return this.selectedCategories.length >= 6
    }
  },
  methods: {
    getBackgroundColor(attr) {
      if (attr) {
        return '#48c78e'
      }
      else {
        return '#fff'
      }
    },
    addRow() {
      this.selectedCategories.push({
        title: this.remainingCategories[Object.keys(this.remainingCategories)[0]],
        count: 0,
        price: 0,
      })
      delete this.remainingCategories[Object.keys(this.remainingCategories)[0]]
    },
    changeCategory(row, category) {
      row.title = category
    },
    removeRow() {
      this.selectedCategories.pop()
    },
    selectLoadingAddress(address){
      this.loading_address = address
    },
    checkForComma(eggsCost) {
      let eggCost = `${eggsCost}`
      if (eggCost.includes(',')) {
        eggCost = eggCost.replace(',', '.')
      }
      return parseFloat(eggCost)
    },
    async sendSellerOrder() {
      this.selectedCategories.forEach(item => {
        switch (item.title) {
          case "CB":
            this.cB = this.cB + +item.count
            this.cB_cost = item.price
            break
          case "C0":
            this.c0 = this.c0 + +item.count
            this.c0_cost = item.price
            break
          case "C1":
            this.c1 = this.c1 + +item.count
            this.c1_cost = item.price
            break
          case "C2":
            this.c2 = this.c2 + +item.count
            this.c2_cost = item.price
            break
          case "C3":
            this.c3 = this.c3 + +item.count
            this.c3_cost = item.price
            break
          case "Грязь":
            this.dirt = this.dirt + +item.count
            this.dirt_cost = item.price
            break
        }
      })

      if (!this.cB && !this.c0 && !this.c1 && !this.c2 && !this.c3 && !this.dirt) {
        return alert('Вы пытаетесь создать пустую заявку')
      }
      if (this.cB && !this.cB_cost) {
        return alert('Вы не указали стоимость за десяток категории СВ')
      }
      if (this.c0 && !this.c0_cost) {
        return alert('Вы не указали стоимость за десяток категории С0')
      }
      if (this.c1 && !this.c1_cost) {
        return alert('Вы не указали стоимость за десяток категории С1')
      }
      if (this.c2 && !this.c2_cost) {
        return alert('Вы не указали стоимость за десяток категории С2')
      }
      if (this.c3 && !this.c3_cost) {
        return alert('Вы не указали стоимость за десяток категории С3')
      }
      if (this.dirt && !this.dirt_cost) {
        return alert('Вы не указали стоимость за десяток категории Грязь')
      }
      if (!this.dates) {
        return alert('Окно поставки не выбрано')
      }
      if (!this.loading_address) {
        return alert('Не выбран адрес производства')
      }
      if (!this.pre_payment_application && this.postponement_pay == null) {
        return alert('Вы не указали отсрочку оплаты')
      }

      const data = {
        current_seller: this.trader.inn,
        cB: this.cB,
        cB_cost: this.cB_cost ? this.checkForComma(this.cB_cost) : 0,
        c0: this.c0,
        c0_cost: this.c0_cost ? this.checkForComma(this.c0_cost) : 0,
        c1: this.c1,
        c1_cost: this.c1_cost ? this.checkForComma(this.c1_cost) : 0,
        c2: this.c2,
        c2_cost: this.c2_cost ? this.checkForComma(this.c2_cost) : 0,
        c3: this.c3,
        c3_cost: this.c3_cost ? this.checkForComma(this.c3_cost) : 0,
        dirt: this.dirt,
        dirt_cost: this.dirt_cost ? this.checkForComma(this.dirt_cost) : 0,
        delivery_window_from: this.dates[0].getDate() + '.' + (this.dates[0].getMonth() + 1) + '.' + this.dates[0].getFullYear(),
        delivery_window_until: this.dates[1].getDate() + '.' + (this.dates[1].getMonth() + 1) + '.' + this.dates[1].getFullYear(),
        loading_address: this.loading_address,
        region: this.trader.region,
        import_application: this.isImport,
        postponement_pay: this.pre_payment_application ? 0 : this.postponement_pay 
      }

      this.loading = true
      const success = await this.$store.dispatch('eggs/postSellerApp', data)
        .finally(() => this.loading = false, setTimeout(this.update, 1000))
      if (!success) return
      this.$emit('close')
    },
    update() {
      this.$store.dispatch('bid/getOwnerTasks')
      this.$store.dispatch('user/getUserNotifications')
    },
    clearFromDateTime() {
      this.dateFrom = null
    }
  }
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.categories {
  &__title {
    margin-bottom: 20px;
    font-size: 20px;
    font-weight: 500;
    border: solid 2px #ebebeb;
    border-radius: 20px;
    background-color: #f5f5f5;
    text-align: center;
  }
  &__content {
    padding: 15px 30px;
    flex-direction: column;
    flex-flow: column;
  }
  &__calendar {
    display: grid;
    grid-template-columns: 1fr;
    gap: 40px;
    margin-top: 20px;
    padding-bottom: 20px;
  }
  &__comment {
    margin-top: 20px;
  }
}

.flexbox {
  display: flex;

  &__column {
    flex-direction: column;
    flex-flow: column;
  }
  &__row {
    flex-direction: row;
    flex-flow: row;
    display: inline-flex;
  }
  &__start {
    justify-content: flex-start;
  }
  &__center {
    justify-content: center;
  }
  &__end {
    justify-content: flex-end;
  }
  &__space-between{
    justify-content: space-between;
  }
}

.card {
  width: 100%;
  float: left;

  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
  &__button-wrapper{
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}

.field {
  min-width: 105px;
}

.bool-button {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 100%;
  height: 30px;
  text-align: center;
  cursor: pointer;
}

.bool-button-half {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 50%;
  height: 30px;
  text-align: center;
  cursor: pointer;
}

.input-border {
  border: solid 2px #ebebeb;
  border-radius: 20px;
  width: 1060px;
  height: 44px;
  margin-bottom: 5px;
}

.my-b-input {
  width: 50%; 
}

.table {
  width: 100%;
  border: solid 2px #ebebeb;
  border-radius: 20px;
  margin-top: 10px;
}

.prod-address {
  height: 26px;
  width: 100%;
  padding-bottom: 0px; 
  margin-bottom: 10px; 
  text-align: center;
  background-color: #f5f5f5;
  border: solid 2px #ebebeb;
  border-top: 0;
  border-radius: 10px;
}

.changeDates {
  display: flex;
  color: #7224f0af;
  font-size: 18px;
  justify-content: center;
  border-radius: 15px;
  background-color: #823bf53a;
}
</style>
