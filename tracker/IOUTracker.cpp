// IoU Tracker C++ impelemntation
// compile with:
// g++ -o x86/IOUTracker.so IOUTracker.cpp -std=c++11 -fPIC -shared -Wall -Wextra `python3.6-config --includes --libs` -lboost_python3
// aarch64-linux-gnu-g++ -o aarch64/IOUTracker.so IOUTracker.cpp -std=c++11 -fPIC -shared -Wall -Wextra `python3.5-config --includes --libs` -lboost_python-py35
// arm-linux-gnueabihf-gcc -o arm7/IOUTracker.so IOUTracker.cpp -std=c++11 -fPIC -shared -Wall -Wextra `python3.7-config --includes --libs` -lboost_python3

#include <boost/python.hpp>
#include <memory>
#include <iostream>
#include <vector>

using namespace std;



// A single detection record
struct Detection
{
    Detection(uint32_t label, float score, float x_min, float y_min, float x_max, float y_max): 
        label{label}, score{score}, x_min{x_min}, y_min{y_min}, x_max{x_max}, y_max{y_max} {}

    uint32_t label;
    float score;
    float x_min, y_min, x_max, y_max;
};

// Track of detections
// Possible states are: active and finished
class Track
{
public:

    Track(Detection& detection): 
        last_detection{detection},
        label{detection.label},
        _max_score{detection.score}, 
        _average_score{detection.score},
        _number_of_detections{1} ,
        _left{(detection.x_max + detection.x_min) / 2},
        _right{(detection.x_max + detection.x_min) / 2},
        _top{(detection.y_max + detection.y_min) / 2},
        _bottom{(detection.y_max + detection.y_min) / 2} {}

    void update(Detection& detection)
    {
        if (detection.label == 0)
            _car_score += detection.score;
        else
            _truck_score += detection.score;
        _number_of_detections++;
        _max_score = max(_max_score, detection.score);
        _average_score = _average_score + ((detection.score - _average_score) / _number_of_detections);
        last_detection = detection;

        float det_x = (detection.x_max + detection.x_min) / 2;
        float det_y = (detection.y_max + detection.y_min) / 2;
        
        _left = min(_left, det_x);
        _right = max(_right, det_x);
        _top = min(_top, det_y);
        _bottom = max(_bottom, det_y);
    }

    bool valid(float sigma_h, uint32_t t_min, uint32_t frame) const
    {
        if ((_max_score >= sigma_h) && (_number_of_detections >= t_min) && (_average_score > 0.5))
        {
            if ((_right - _left < 0.3) && (_bottom - _top < 0.3))
            {
                //cout << "would be valid truck but is not moving" << endl;
                //cout << frame << endl;
                return false;
            }
            return true;
        }
        return false;
    }
    bool active_valid(float sigma_h) const
    {
        return (_max_score >= sigma_h);
    }

    bool car_has_better_score()
    {
        return _car_score > _truck_score;
    }
    
    Detection last_detection;
    uint32_t label;
private:
    float _max_score;
    float _average_score;
    uint32_t _number_of_detections;

    float _left;
    float _right;
    float _top;
    float _bottom;

    float _car_score = 0;
    float _truck_score = 0;
};


class IOUTracker
{
public:
    IOUTracker(float sigma_l, float sigma_h, float sigma_iou, uint32_t t_min, bool multiple_object_type):
        _sigma_l{sigma_l}, 
        _sigma_h{sigma_h}, 
        _sigma_iou{sigma_iou}, 
        _t_min{t_min}, 
        _frame_number{0}, 
        _multiple_object_type{multiple_object_type},
        _active_tracks{vector<Track>()}
    {
        cout << "C++ tracker implementation" << endl;
    }

    uint32_t update_tracks(boost::python::list p_detections)
    {
        _frame++;
        auto detections = this->__parse_detections(p_detections);
        auto ended_tracks = std::vector<uint32_t>();
        uint32_t detection_size = detections->size(); 
        uint32_t index = 0;
        for (auto & track : this->_active_tracks)
        {

            // find best detection box for given track
            float best_match_score = -1.0;
            uint32_t best_detection_index;
            for (uint32_t i = 0; i < detection_size; i++)
            {
                float match = this->__iou(detections->at(i), track.last_detection);
                if (match > best_match_score)
                {
                    best_match_score = match;
                    best_detection_index = i;
                }
            }
            // given track can be updated
            if (best_match_score >= this->_sigma_iou)
            {
                track.update(detections->at(best_detection_index));
                detections->erase(detections->begin() + best_detection_index);
                detection_size--;
            }
            else
            {
                if (track.valid(this->_sigma_h, this->_t_min, _frame))
                {
                    if (_multiple_object_type)
                    {
                        if (track.car_has_better_score())
                            _finished_cars++;
                        else
                        {
                            cout << "trucks ends " << _frame << endl;
                            _finished_trucks++;
                        }
                    }
                    this->_finished_tracks++;
                }
                ended_tracks.push_back(index);
            }
            index++;
        }

        // Delete finished tracks from active tracks
        for (auto i = ended_tracks.rbegin(); i != ended_tracks.rend(); ++i ) 
        {
            this->_active_tracks.erase(this->_active_tracks.begin() + *i);
        }        
        // Create new tracks from unresolved detections
        for (auto & det : *detections)
        {
            this->_active_tracks.emplace_back(det);
        }
        return this->_finished_tracks;
    }

    uint32_t get_finished_tracks(){ return _finished_tracks; }
    uint32_t get_finished_cars(){ return _finished_cars; }
    uint32_t get_finished_trucks(){ return _finished_trucks; }

    uint32_t get_active_tracks(){ return _get_active_tracks(10); }
    uint32_t get_active_cars(){ return _get_active_tracks(0); }
    uint32_t get_active_trucks(){ return _get_active_tracks(1); }


private:
    unique_ptr<vector<Detection>> __parse_detections(boost::python::list p_detections)
    {
        unique_ptr<vector<Detection>> detections(new vector<Detection>());

        boost::python::ssize_t len = boost::python::len(p_detections);
        for (int i = 0; i < len; i += 6)
        {
            float score = boost::python::extract<float>(p_detections[i + 1]);
            if (score >= this->_sigma_l)
            {
                uint32_t label = boost::python::extract<uint32_t>(p_detections[i]);
                float xmin = boost::python::extract<float>(p_detections[i + 2]);
                float ymin = boost::python::extract<float>(p_detections[i + 3]);
                float xmax = boost::python::extract<float>(p_detections[i + 4]);
                float ymax = boost::python::extract<float>(p_detections[i + 5]);
                detections->emplace_back(label, score, xmin, ymin, xmax, ymax);
            }
        }
        return move(detections);
    }

    float __iou(Detection& bbox1, Detection& bbox2)
    {
        float overlap_x0 = max(bbox1.x_min, bbox2.x_min);
        float overlap_y0 = max(bbox1.y_min, bbox2.y_min);
        float overlap_x1 = min(bbox1.x_max, bbox2.x_max);
        float overlap_y1 = min(bbox1.y_max, bbox2.y_max);
        // check if there is an overlap
        if ((overlap_x1 - overlap_x0 <= 0) || (overlap_y1 - overlap_y0 <= 0))
            return 0.0;
        float size_1 = (bbox1.x_max - bbox1.x_min) * (bbox1.y_max - bbox1.y_min);
        float size_2 = (bbox2.x_max - bbox2.x_min) * (bbox2.y_max - bbox2.y_min);
        float size_intersection = (overlap_x1 - overlap_x0) * (overlap_y1 - overlap_y0);
        float size_union = size_1 + size_2 - size_intersection;
        return size_intersection / size_union;
    }

    uint32_t _get_active_tracks(uint32_t label)
    {
        bool all_labels = (label == 10);
        uint32_t valid_tracks = 0;
        for (auto const & track : this->_active_tracks)
        {
            if (track.active_valid(this->_sigma_h) && (all_labels || track.label == label))
                valid_tracks++;
        }
        return valid_tracks;
    }


    float _sigma_l;
    float _sigma_h;
    float _sigma_iou;
    uint32_t _t_min;

    uint32_t _finished_tracks = 0;
    uint32_t _finished_cars = 0;
    uint32_t _finished_trucks = 0;
    uint32_t _frame_number;
    bool _multiple_object_type;
    vector<Track> _active_tracks;
    uint32_t _frame = 0;
};


// Export IOUTracker using boost library
BOOST_PYTHON_MODULE(IOUTracker)
{
    using namespace boost::python;
    class_<IOUTracker>("IOUTracker", init<float, float, float, uint32_t, bool>())
        .def("update_tracks", &IOUTracker::update_tracks, "This is the docstring for A::get_i")
        .def("get_finished_tracks", &IOUTracker::get_finished_tracks, "This is the docstring for A::get_i")
        .def("get_finished_cars", &IOUTracker::get_finished_cars, "This is the docstring for A::get_i")
        .def("get_finished_trucks", &IOUTracker::get_finished_trucks, "This is the docstring for A::get_i")
        .def("get_active_tracks", &IOUTracker::get_active_tracks, "This is the docstring for A::get_i")
        .def("get_active_cars", &IOUTracker::get_active_cars, "This is the docstring for A::get_i")
        .def("get_active_trucks", &IOUTracker::get_active_trucks, "This is the docstring for A::get_i");
}
