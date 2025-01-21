import streamlit as st
import utils.db.queries as db


# ====================

def input_other(_cookie):
    cookie = _cookie

    # ===== UTILITY DB FUNCTIONS =====

    def load_from_db():
        return db.load_intos(cookie.get('user_ID'))

    def load_to_db(_data):
        db.update_intos(cookie.get('user_ID'), _data)

    # ===== END of UTILITY DB FUNCTIONS =====

    data = {}
    intos = load_from_db()

    # ----------

    st.header("What are you looking for?")

    tab1, tab2 = st.columns(2, gap='medium')

    with tab1:
        data['gender'] = st.radio("Gender", ["Male", "Female", ":rainbow[All]"], key="gender",
                                  index=((int(intos['gender']) - 1) if intos['gender'] else 0))
        data['age'] = st.number_input("Age", key="age", min_value=18, max_value=100, step=1,
                                      value=(intos['age'] if (intos['age']) else 30))
        data['age_flag'] = st.checkbox("Specify a range for age", key="age_flag", value=intos['age_flag'])

        if data['age_flag']:
            data['age_radius'] = st.slider("Age Interval", key="age_radius", min_value=1, max_value=100,
                                           value=(intos['age_radius'] if intos['age_radius'] else 1), step=1)
        else:
            data['age_radius'] = 0

    with tab2:
        data['distance_flag'] = st.checkbox("Partners close to you", key="distance_flag", value=intos['distance_flag'])

        if data['distance_flag']:
            data['distance_km'] = st.slider("MAX Distance in km", key="distance_km", min_value=10, max_value=1000,
                                            value=(intos['distance_km'] if intos['distance_km'] else 10), step=10)
        else:
            data['distance_km'] = 0

    tab1, tab2 = st.columns(2, gap='large')

    with tab1:
        st.subheader("Are those features important for you?")
        st.text("1 means 'Not at all', 5 means 'Definitely yes'")

        data['attractiveness_important'] = st.slider("Attractiveness", key="attractiveness_important", min_value=1,
                                                     max_value=5, value=(
                intos['attractiveness_important'] if intos['attractiveness_important'] else 3), step=1)
        data['sincerity_important'] = st.slider("Sincerity", key="sincerity_important", min_value=1,
                                                max_value=5, value=(
                intos['sincerity_important'] if intos['sincerity_important'] else 3), step=1)
        data['intelligence_important'] = st.slider("Intelligence", key="intelligence_important", min_value=1,
                                                   max_value=5, value=(
                intos['intelligence_important'] if intos['intelligence_important'] else 3), step=1)
        data['funniness_important'] = st.slider("Funniness", key="funniness_important", min_value=1,
                                                max_value=5, value=(
                intos['funniness_important'] if intos['funniness_important'] else 3), step=1)
        data['ambition_important'] = st.slider("Ambition", key="ambition_important", min_value=1,
                                               max_value=5, value=(
                intos['ambition_important'] if intos['ambition_important'] else 3), step=1)

    with tab2:
        st.subheader("What should be the interests of your perfect partner?")

        data['same_interest'] = st.checkbox("Same as mine", key="same_interest", value=intos['same_interest'])

        if not data['same_interest']:
            data['sports'] = st.slider("Sports", key="sports", min_value=1, max_value=10,
                                       value=(intos['sports'] if intos['sports'] else 5), step=1)
            data['tv_sports'] = st.slider("TV Sports", key="tv_sports", min_value=1, max_value=10,
                                          value=(intos['tv_sports'] if intos['tv_sports'] else 5), step=1)
            data['exercise'] = st.slider("Exercise", key="exercise", min_value=1, max_value=10,
                                         value=(intos['exercise'] if intos['exercise'] else 5), step=1)
            data['dining'] = st.slider("Dining", key="dining", min_value=1, max_value=10,
                                       value=(intos['dining'] if intos['dining'] else 5), step=1)
            data['art'] = st.slider("Art", key="art", min_value=1, max_value=10,
                                    value=(intos['art'] if intos['art'] else 5), step=1)
            data['hiking'] = st.slider("Hiking", key="hiking", min_value=1, max_value=10,
                                       value=(intos['hiking'] if intos['hiking'] else 5), step=1)
            data['gaming'] = st.slider("Gaming", key="gaming", min_value=1, max_value=10,
                                       value=(intos['gaming'] if intos['gaming'] else 5), step=1)
            data['clubbing'] = st.slider("Clubbing", key="clubbing", min_value=1, max_value=10,
                                         value=(intos['clubbing'] if intos['clubbing'] else 5), step=1)
            data['reading'] = st.slider("Reading", key="reading", min_value=1, max_value=10,
                                        value=(intos['reading'] if intos['reading'] else 5), step=1)
            data['tv'] = st.slider("TV", key="tv", min_value=1, max_value=10,
                                   value=(intos['tv'] if intos['tv'] else 5), step=1)
            data['theater'] = st.slider("Theater", key="theater", min_value=1, max_value=10,
                                        value=(intos['theater'] if intos['theater'] else 5), step=1)
            data['movies'] = st.slider("Movies", key="movies", min_value=1, max_value=10,
                                       value=(intos['movies'] if intos['movies'] else 5), step=1)
            data['music'] = st.slider("Music", key="music", min_value=1, max_value=10,
                                      value=(intos['music'] if intos['music'] else 5), step=1)
            data['shopping'] = st.slider("Shopping", key="shopping", min_value=1, max_value=10,
                                         value=(intos['shopping'] if intos['shopping'] else 5), step=1)
            data['yoga'] = st.slider("Yoga", key="yoga", min_value=1, max_value=10,
                                     value=(intos['yoga'] if intos['yoga'] else 5), step=1)

    if st.button("Save", use_container_width=True):
        load_to_db(data)
