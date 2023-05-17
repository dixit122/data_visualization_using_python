import streamlit as st
import pandas as pd
import plotly.express as px

# readind the data from the csv file
data = pd.read_csv('DataSet1.csv')

# making an array of the device ids
device_id = data['Device_id'].unique().tolist()

# Convert 'time' column to datetime objects
data['time'] = pd.to_datetime(data['time'], format='%d-%m-%Y %H:%M')


def plot_the_graphs(selected_device):

    if selected_device == "Comparison":
        # Calculate the cumulative average of 'RPM' column for all devices
        all_devices_data = data.groupby('Device_id').apply(
            lambda x: x.assign(Cumulative_Average=x['RPM'].expanding().mean())
        ).reset_index(drop=True)

        # Plot average RPM vs Time for all devices
        average_RPM_comparison = px.line(all_devices_data, x='time', y='Cumulative_Average', color='Device_id',
                                         title="Average RPM Comparison")
        average_RPM_comparison.update_layout(
            xaxis_title='Time',
            yaxis_title='Average RPM',
        )
        st.plotly_chart(average_RPM_comparison)

        # Plot efficiency vs Time for all devices
        all_devices_data['Efficiency'] = all_devices_data['On_time'] / \
            (all_devices_data['On_time'] + all_devices_data['Off_time'])
        efficiency_comparison = px.line(all_devices_data, x='time', y='Efficiency', color='Device_id',
                                        title="Efficiency Comparison")
        st.plotly_chart(efficiency_comparison)

        # Plot RPM vs Time for all devices
        RPM_comparison = px.line(all_devices_data, x='time', y='RPM', color='Device_id',
                                 title="RPM Comparison")
        st.plotly_chart(RPM_comparison)

        # Plot Total Rotations vs Time for all devices
        Total_rotations_comparison = px.line(all_devices_data, x='time', y='Total_rotations', color='Device_id',
                                             title='Total Rotations Comparison')
        st.plotly_chart(Total_rotations_comparison)
    elif selected_device != "raw data":

        device_data = data[data['Device_id'] == selected_device]

        # Calculate the cumulative average of 'RPM' column
        device_data['Cumulative Average'] = device_data.loc[device_data.loc[:, 'Device_id']
                                                            == selected_device, 'RPM'].expanding().mean()

        # average RPM
        average_RPM = px.line(device_data, x='time', y='Cumulative Average',
                              title="Average RPM vs Time")
        average_RPM.update_layout(
            xaxis_title='Time',  # Change x-axis label
            yaxis_title='Average RPM',  # Change y-axis label
        )
        st.plotly_chart(average_RPM)

        # calculating the device efficiency
        device_data['Efficiency'] = device_data['On_time'] / \
            (device_data['On_time'] + device_data['Off_time'])

        # plot efficiency vs Time
        efficiency = px.line(device_data, x='time', y='Efficiency',
                             title="Efficiency vs Time")
        st.plotly_chart(efficiency)

        # Plot RPM vs Time
        RPM_time = px.line(device_data, x='time', y='RPM',
                           title="RPM vs Time")

        st.plotly_chart(RPM_time)

        # Plot Total Rotations vs. Time
        Total_rot_Time = px.line(device_data, x='time', y='Total_rotations',
                                 title='Total Rotations vs Time')
        st.plotly_chart(Total_rot_Time)

    else:
        st.write(data)


def main():
    # title of the webpage
    st.write("# Welcome to my application")  # Increase heading size

    # making a list for the sidebar selection
    side_bar_list = device_id + ["raw data", "Comparison"]

    # making sidebar to give user access to selecting different devices
    selected_item = st.sidebar.selectbox("Select an option", side_bar_list)

    plot_the_graphs(selected_item)


if __name__ == "__main__":
    main()
