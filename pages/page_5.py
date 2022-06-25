import streamlit as st
from scripts import config


def value():
    if not config in st.session_state:
        st.session_state.config = config.default_params
    else:
        st.write(f"gamma is  : {st.session_state.config['gamma']} ")
    # st.write(f" module gama {config.likelihood_params['gamma']}")
    form = st.form(key='my-form')
    gamma = form.text_input('Enter the value of gamma', value=st.session_state.config['gamma'])
    #st.write(f"config is  {config.likelihood_params} ")
    c = form.text_input('Enter the value of c ', value=st.session_state.config['c'])
    k = form.text_input('Enter the value of k ', value=st.session_state.config['k'])
    bn_mean = form.text_input('Initial value of bn(mean)', value=st.session_state.config['bn_mean'])
    bn_std = form.text_input('Initial value of bn(std)', value=st.session_state.config['bn_std'])

    validate = form.form_submit_button(label='Submit')
    st.write('Press submit to validate')
    if validate:
        st.write(f'The value of gamma is: {gamma}')
        st.write(f'The value of k is: {k}')
        st.write(f'The value of c is: {c}')
        st.write(f'The value of bn is: {bn_mean}')
        st.write(f'The value of bn(2nd) argument  is: {bn_std}')

        added_param = config.default_params
        added_param['gamma'] = float(gamma)
        added_param['k'] = float(k)
        added_param['c'] = float(c)
        added_param['bn_mean'] = float(bn_mean)
        added_param['bn_std'] = bn_std
        st.session_state.config = added_param
       # config.likelihood_params['gamma'] = gamma






# Value computed using the paper and experimental data.

