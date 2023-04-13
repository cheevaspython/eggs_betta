<template>
  <form action="">
    <div class="modal-card" style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Создать Заявку</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')"/>
      </header>
      <section class="modal-card-body is-fullwidth">
        <!--        <pre>{{trader}}</pre>-->
        <!--        Ячейка Категория Количество Цена-->


        <div class="categories__content">
          <h1 class="categories__title"><strong>ИНН: {{ trader.inn }} </strong>
            {{ trader.name }}</h1>
          <div v-for="(row,index) in selectedCategories" class="categories__row">
            <!--            dropdown-->

            <b-dropdown aria-role="list" class="categories__dropdown" v-model="row.title">
              <template #trigger="{ active }">
                <b-field label="Категория">
                  <b-button
                    :label="row.title"
                    :icon-right="active ? 'menu-up' : 'menu-down'"/>
                </b-field>
              </template>


              <b-dropdown-item v-for="(category) in categories" aria-role="listitem" @click="row.title = category">
                {{
                  category
                }}
              </b-dropdown-item>


            </b-dropdown>

            <b-field label="Количество" class="mb-1">
              <b-input v-model="row.count" type="number" maxlength="10" class="mr-4"></b-input>
            </b-field>
            <b-field label="Цена">
              <b-input v-model="row.price" type="number" maxlength="10"></b-input>
            </b-field>

          </div>


          <b-button class="button is-info is-light mr-2" icon-left="plus" @click="addRow">Добавить категорию</b-button>
          <b-button class="button is-info is-light" icon-left="minus" @click="removeRow" :disabled="removeBtnDisabled">
            Убрать категорию
          </b-button>

          <div class="categories__calendar">
            <b-field label="Выберите диапазон дат">
              <b-datepicker
                placeholder="Кликните чтобы выбрать"
                v-model="dates"
                icon="calendar-today"
                append-to-body
                range>
              </b-datepicker>
            </b-field>
            <!--            <b-field label="Дата начала">-->
            <!--              <b-datetimepicker-->
            <!--                v-model="dateFrom"-->
            <!--                placeholder="Нажмите для выбора"-->
            <!--                icon="calendar-today"-->
            <!--                :first-day-of-week="1"-->
            <!--                @icon-right-click="clearFromDateTime"-->
            <!--                :icon-right="dateFrom ? 'close-circle' : ''">-->
            <!--              </b-datetimepicker>-->
            <!--            </b-field>-->
            <!--            <b-field label="Дата окончания">-->
            <!--              <b-datetimepicker-->
            <!--                class="block"-->
            <!--                v-model="dateTo"-->
            <!--                placeholder="Нажмите для выбора"-->
            <!--                icon="calendar-today"-->
            <!--                :first-day-of-week="1"-->
            <!--                @icon-right-click="clearFromDateTime"-->
            <!--                :icon-right="dateFrom ? 'close-circle' : ''">-->
            <!--              </b-datetimepicker>-->
            <!--            </b-field>-->
          </div>

          <div class="categories__comment">
            <b-field label="Комментарий">
              <b-input type="textarea" v-model="comment"></b-input>
            </b-field>
          </div>
        </div>

      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Отправить заявку"
          :loading="loading"
          type="is-info"
          @click="sendOrder"/>
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>

<script>
export default {
  name: "ModalForm",
  props: ['trader'],
  data() {
    return {
      loading: false,
      testValue: 'testv',
      isPublic: true,
      dateFrom: new Date(),
      dateTo: new Date(),
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
      dates: [],
      email: '',
      password: '',
      selectedCategories: [{
        title: 'C0',
        count: '',
        price: '',
      }],
      comment: '',

      categories: ['C0', 'C1', 'C2', 'C3', 'Грязюка'],

    }
  },
  computed: {
    removeBtnDisabled() {
      return this.selectedCategories.length <= 1
    },
    setLabel(index) {
    }
  },
  methods: {
    addRow() {
      this.selectedCategories.push({
        count: '',
        price: '',
        title: 'C0'
      })
    },
    removeRow() {
      this.selectedCategories.pop()
    },
    sendOrder() {
      // this.$axios.post('')

      this.selectedCategories.forEach(item => {
        console.log('####### item.title ', item.title)
        switch (item.title) {
          case "C0":
            this.c0 = this.c0 + +item.count
            this.c0_cost = +item.price
            break
          case "C1":
            this.c1 = this.c1 + +item.count
            this.c1_cost = +item.price
            break
          case "C2":
            this.c2 = this.c2 + +item.count
            this.c2_cost = +item.price
            break
          case "C3":
            this.c3 = this.c3 + +item.count
            this.c3_cost = +item.price
            break
          case "Грязюка":
            this.dirt = this.dirt + +item.count
            this.dirt_cost = +item.price
            break
        }
      })

      const data = {
        c0: this.c0,
        c0_cost: this.c0_cost,
        c1: this.c1,
        c1_cost: this.c1_cost,
        c2: this.c2,
        c2_cost: this.c2_cost,
        c3: this.c3,
        c3_cost: this.c3_cost,
        dirt: this.dirt,
        dirt_cost: this.dirt_cost,
        seller: this.trader.id,
        delivery_window_from: this.dates[0],
        delivery_window_until: this.dates[1]
      }
      this.loading = true
      this.$store.dispatch('eggs/postSellerApp', data)
        .finally(() => this.loading = false)
      // console.log('####### this ', this)
      // console.log('####### this.selectedCategories ', {
      //   trader: this.trader,
      //   categories: this.selectedCategories,
      //   dates: this.dates,
      //   comment: this.comment
      // })
    },
    clearFromDateTime() {
      this.dateFrom = null
    }
  },
  mounted() {
    console.log('####### this.trader ', this.trader)
  }

}
</script>

<style lang="scss" scoped>
.categories {
  &__title {
    margin-bottom: 20px;
    font-size: 20px;
    font-weight: 500;
  }

  &__content {
    padding: 15px 30px;
  }

  &__row {
    display: grid;
    grid-template-columns: 100px 1fr 1fr;
    place-items: center;
    gap: 15px;
    padding-bottom: 15px;
    margin-bottom: 15px;
    border-bottom: 1px solid #EFF0F5;
  }

  &__dropdown {
    vertical-align: center;
    display: block;
    align-self: center;
    padding-bottom: 3px;
  }

  //button {
  //  border: 1px solid pink;
  //  vertical-align: center;
  //}
  &__calendar {
    display: grid;
    grid-template-columns: 1fr;
    gap: 40px;
    margin-top: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #EFF0F5;
  }

  &__comment {
    margin-top: 20px;
  }
}
</style>
